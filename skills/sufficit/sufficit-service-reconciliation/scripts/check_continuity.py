#!/usr/bin/env python3
"""Read-only acceptance checks over provider captures and real UI assessment rows."""
import argparse
import calendar
import datetime as dt
import json
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

BR = ZoneInfo('America/Sao_Paulo')


def civil(value):
    # Contract/history DTO dates are civil labels, even when serialized with Z.
    return dt.date.fromisoformat(value[:10])


def read(path):
    return json.loads(path.read_text(encoding='utf-8'), parse_float=Decimal)


def stable(value):
    return json.dumps(value, sort_keys=True, default=str, ensure_ascii=False)


def review(capture, baseline, contract_ids, since, now, indefinite=False):
    if now.tzinfo is None:
        raise ValueError('--as-of requires an explicit offset')
    today = now.astimezone(BR).date()
    findings = []

    def fail(code, **context):
        findings.append(dict(code=code, **context))

    contracts = {x['Id']: x for x in read(capture / 'contracts.json')}
    customers = {x['Id']: x for x in read(capture / 'customers.json')}
    assessment = {x['ContractId']: x for x in read(capture / 'financial-assessment.json')}
    for cid in contract_ids:
        if cid not in contracts or cid not in assessment:
            fail('missing_contract_or_ui_assessment', contract=cid)
            continue
        contract = contracts[cid]
        customer = customers[contract['ContextId']]
        preference = customer.get('DueDay', customer.get('dueday'))
        if preference is None:
            fail('missing_customer_preference', contract=cid)
            continue
        if contract.get('DueDay') != preference:
            fail('due_day_differs_from_preference', contract=cid)
        if indefinite and contract.get('End') is not None:
            fail('indefinite_contract_has_end', contract=cid)
        if contract.get('NextDueDate'):
            date = civil(contract['NextDueDate'])
            if date.day != min(int(preference), calendar.monthrange(date.year, date.month)[1]):
                fail('next_due_day_differs_from_preference', contract=cid)
        alignment = json.loads(contract.get('ParameterValues', {}).get('billing.scheduleAlignment.v1', '{}'))
        cycle_day = alignment.get('CycleDay') or alignment.get('DueDay')
        if not cycle_day or alignment.get('DueDay') != preference:
            fail('missing_or_inconsistent_cycle_anchor', contract=cid)
        rows = sorted((r for r in assessment[cid]['Entries'] if civil(r['End']) > since), key=lambda r: civil(r['Start']))
        if not rows:
            fail('no_entries_in_proved_scope', contract=cid)
            continue
        if contract.get('NextDueDate') and cycle_day:
            due = civil(contract['NextDueDate'])
            year, month = due.year, due.month
            expected = dt.date(year, month, min(int(cycle_day), calendar.monthrange(year, month)[1]))
            if int(cycle_day) != int(preference) and expected <= due:
                year, month = (year + 1, 1) if month == 12 else (year, month + 1)
                expected = dt.date(year, month, min(int(cycle_day), calendar.monthrange(year, month)[1]))
            if alignment.get('GenerateFrom') and expected < civil(alignment['GenerateFrom']):
                fail('next_due_precedes_native_generation_boundary', contract=cid)
            if not any(civil(r['Start']) == expected for r in rows):
                fail('next_due_without_corresponding_coverage', contract=cid, expected=str(expected))
        ledger = read(capture / ('ledger-' + contract['ContextId'] + '.json'))
        cursor = since
        for row in rows:
            start, end = civil(row['Start']), civil(row['End'])
            if end <= start:
                fail('non_positive_coverage', contract=cid, entry=row['Id'])
            if start > cursor:
                fail('coverage_gap', contract=cid, start=str(cursor), end=str(start))
            elif start < cursor and cursor != since:
                fail('coverage_overlap', contract=cid, entry=row['Id'])
            cursor = max(cursor, end)
            if cycle_day and any(d.day != min(int(cycle_day), calendar.monthrange(d.year, d.month)[1]) for d in (start, end)):
                fail('entry_outside_reviewed_cycle', contract=cid, entry=row['Id'])
            docs = set(row['Documents'])
            # Exact commercial document identities; never match by amount/date.
            linked = [r for r in ledger if r.get('Active') and r.get('Document') in docs and r.get('Kind', '').startswith('ativ')]
            if start > today and linked:
                fail('future_service_already_in_ledger', contract=cid, entry=row['Id'], records=[r['Id'] for r in linked])
            if row['State'] in ('Missing', 'Divergent', 'InactiveOnly', 'Unavailable'):
                fail('ui_financial_finding', contract=cid, entry=row['Id'], state=row['State'])
            amount = Decimal(str(row['Amount']))
            if start <= today and amount and sum((Decimal(str(r['Value'])) for r in linked), Decimal(0)) != -amount:
                fail('past_service_without_exact_active_debit', contract=cid, entry=row['Id'])

    baseline_ledgers = list(baseline.glob('ledger-*.json'))
    if not baseline_ledgers:
        fail('missing_baseline_ledgers')
    if {x.name for x in baseline_ledgers} != {x.name for x in capture.glob('ledger-*.json')}:
        fail('wallet_scope_changed')
    for before_file in baseline_ledgers:
        after_file = capture / before_file.name
        if not after_file.exists():
            fail('missing_wallet_capture', file=before_file.name)
            continue
        before, after = read(before_file), read(after_file)
        # AccumulatedBefore is derived from ordering; every persisted field is compared.
        canon = lambda rows: stable(sorted(({k: v for k, v in r.items() if k != 'AccumulatedBefore'} for r in rows), key=lambda r: r['Id']))
        if canon(before) != canon(after):
            fail('ledger_changed_in_calendar_only_repair', file=before_file.name)
    for name in ('renewals.json', 'original-purchases.json'):
        if stable(read(baseline / name)) != stable(read(capture / name)):
            fail('original_receipts_changed', file=name)
    originals = {x['Id']: x for x in read(baseline / 'contracts.json')}
    for cid in contract_ids:
        if cid not in contracts or cid not in originals:
            continue
        key = 'history.service-lineage.v1'
        old = json.loads(originals[cid].get('ParameterValues', {}).get(key, '{"Purchases":[]}'))
        new = json.loads(contracts[cid].get('ParameterValues', {}).get(key, '{"Purchases":[]}'))
        purchases = {x['Id']: x for x in new['Purchases']}
        for purchase in old['Purchases']:
            current = purchases.get(purchase['Id'])
            if current is None or any(current[k] != purchase[k] for k in ('Start', 'End', 'Amount')):
                fail('original_purchase_rewritten', contract=cid, purchase=purchase['Id'])
    return dict(passed=not findings, findings=findings, contracts=contract_ids, since=str(since), as_of=now.isoformat(),
                checks=['ui_coverage_continuity', 'preferred_day_and_cycle', 'next_due_matches_projected_coverage', 'future_service_not_emitted', 'exact_past_debits',
                        'complete_ledger_unchanged', 'original_receipts_unchanged', 'original_purchase_fields_unchanged'],
                not_checked=['agreement_authorization', 'representative_funding_order', 'durable_consumer_execution',
                             'telephony_credit_delivery', 'global_commercial_replay'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', required=True, type=Path)
    parser.add_argument('--baseline', required=True, type=Path)
    parser.add_argument('--contract', required=True, action='append')
    parser.add_argument('--since', required=True, type=dt.date.fromisoformat)
    parser.add_argument('--as-of', required=True)
    parser.add_argument('--expect-indefinite', action='store_true')
    parser.add_argument('--report', required=True, type=Path)
    args = parser.parse_args()
    # Exclusive creation: an earlier acceptance report remains evidence.
    if args.report.exists():
        parser.error('report already exists; preserve prior evidence')
    try:
        result = review(args.capture, args.baseline, args.contract, args.since,
                        dt.datetime.fromisoformat(args.as_of.replace('Z', '+00:00')), args.expect_indefinite)
    except (OSError, ValueError, KeyError, TypeError) as error:
        result = dict(passed=False, findings=[dict(code='unavailable_or_invalid_input', detail=str(error))])
    with args.report.open('x', encoding='utf-8') as output:
        json.dump(result, output, indent=2, ensure_ascii=False)
    print(json.dumps(dict(passed=result['passed'], findings=len(result['findings']), report=str(args.report))))
    raise SystemExit(0 if result['passed'] else 2)


if __name__ == '__main__':
    main()
