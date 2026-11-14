import copy
import datetime as dt
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/sufficit/sufficit-service-reconciliation/scripts/check_continuity.py'
review = runpy.run_path(str(SCRIPT))['review']


class ContinuityAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.before = self.root / 'before'
        self.after = self.root / 'after'
        self.since = dt.date(2026, 9, 27)
        self.now = dt.datetime.fromisoformat('2026-11-14T18:00:00-03:00')
        self.data = {
            'contracts': [{'Id': 'service', 'ContextId': 'customer', 'DueDay': 26,
                           'NextDueDate': '2026-12-26T00:00:00Z', 'End': None,
                           'ParameterValues': {'billing.scheduleAlignment.v1': json.dumps({'DueDay': 26, 'CycleDay': 27, 'GenerateFrom': '2026-12-27'}),
                                               'history.service-lineage.v1': json.dumps({'Purchases': [{'Id': 'purchase', 'Start': '2026-09-28', 'End': '2026-10-27', 'Amount': 30}]})}}],
            'customers': [{'Id': 'customer', 'DueDay': 26}],
            'renewals': [{'Id': 'immutable', 'Value': 30}],
            'original-purchases': [{'Id': 'original', 'Value': 30}],
            'ledger-customer': [
                {'Id': 'credit', 'Timestamp': '2026-09-26T08:59:00Z', 'Value': 60, 'Kind': 'trne', 'Document': 'transfer', 'Active': True},
                {'Id': 'first', 'Timestamp': '2026-09-26T09:00:00Z', 'Value': -30, 'Kind': 'ativ', 'Document': 'SERVICO:first', 'Active': True},
                {'Id': 'second', 'Timestamp': '2026-10-02T09:00:00Z', 'Value': -30, 'Kind': 'ativ', 'Document': 'SERVICO:second', 'Active': True}],
            'ledger-representative': [{'Id': 'out', 'Value': -60, 'Kind': 'trns', 'Active': True}],
            'financial-assessment': [{'ContractId': 'service', 'Entries': [
                {'Id': 'first', 'Start': '2026-09-27', 'End': '2026-10-27', 'Amount': 30, 'Documents': ['SERVICO:first'], 'State': 'Matched'},
                {'Id': 'second', 'Start': '2026-10-27', 'End': '2026-11-27', 'Amount': 30, 'Documents': ['SERVICO:second'], 'State': 'Matched'},
                {'Id': 'future', 'Start': '2026-11-27', 'End': '2026-12-27', 'Amount': 30, 'Documents': ['SERVICO:future'], 'State': 'Future'},
                {'Id': 'next', 'Start': '2026-12-27', 'End': '2027-01-27', 'Amount': 30, 'Documents': ['SERVICO:next'], 'State': 'Future'}]}]
        }
        for folder in (self.before, self.after):
            folder.mkdir()
            for name, value in self.data.items():
                (folder / (name + '.json')).write_text(json.dumps(value))

    def write(self, name, value):
        (self.after / (name + '.json')).write_text(json.dumps(value))

    def result(self):
        return review(self.after, self.before, ['service'], self.since, self.now, True)

    def codes(self):
        return {x['code'] for x in self.result()['findings']}

    def test_valid_separate_due_and_cycle_preserves_money(self):
        self.assertTrue(self.result()['passed'])
        self.assertIn('representative_funding_order', self.result()['not_checked'])

    def test_provider_capture_lowercase_dueday_is_supported(self):
        self.write('customers', [{'Id': 'customer', 'dueday': 26}])
        self.assertTrue(self.result()['passed'])

    def test_one_day_gap_is_not_hidden_by_matched_finance(self):
        rows = copy.deepcopy(self.data['financial-assessment'])
        rows[0]['Entries'][1]['Start'] = '2026-10-28'
        self.write('financial-assessment', rows)
        self.assertIn('coverage_gap', self.codes())
        self.assertIn('entry_outside_reviewed_cycle', self.codes())

    def test_future_record_is_error_even_if_timestamp_was_moved(self):
        rows = self.data['ledger-customer'] + [{'Id': 'early', 'Timestamp': '2026-11-27T09:00:00Z', 'Value': -30, 'Kind': 'ativ', 'Document': 'SERVICO:future', 'Active': True}]
        self.write('ledger-customer', rows)
        self.assertIn('future_service_already_in_ledger', self.codes())

    def test_unchanged_balance_does_not_hide_changed_document(self):
        rows = copy.deepcopy(self.data['ledger-customer'])
        rows[0]['Document'] = 'different'
        self.write('ledger-customer', rows)
        self.assertIn('ledger_changed_in_calendar_only_repair', self.codes())

    def test_missing_capture_cannot_pass(self):
        (self.after / 'renewals.json').unlink()
        with self.assertRaises(FileNotFoundError):
            self.result()

    def test_preferred_day_and_contract_end_are_independent(self):
        rows = copy.deepcopy(self.data['contracts'])
        rows[0]['DueDay'] = 27
        rows[0]['End'] = '2026-12-27'
        self.write('contracts', rows)
        self.assertIn('due_day_differs_from_preference', self.codes())
        self.assertIn('indefinite_contract_has_end', self.codes())

    def test_correct_preferred_day_with_wrong_month_still_fails(self):
        rows = copy.deepcopy(self.data['contracts'])
        rows[0]['NextDueDate'] = '2027-01-26'
        self.write('contracts', rows)
        self.assertIn('next_due_without_corresponding_coverage', self.codes())

    def test_already_reserved_cycle_is_not_the_next_native_renewal(self):
        rows = copy.deepcopy(self.data['contracts'])
        rows[0]['NextDueDate'] = '2026-11-26'
        self.write('contracts', rows)
        self.assertIn('next_due_precedes_native_generation_boundary', self.codes())

    def test_original_receipt_is_protected(self):
        self.write('renewals', [{'Id': 'immutable', 'Value': 31}])
        self.assertIn('original_receipts_changed', self.codes())

    def test_raw_purchase_dates_cannot_be_overwritten(self):
        rows = copy.deepcopy(self.data['contracts'])
        history = json.loads(rows[0]['ParameterValues']['history.service-lineage.v1'])
        history['Purchases'][0]['Start'] = '2026-09-27'
        rows[0]['ParameterValues']['history.service-lineage.v1'] = json.dumps(history)
        self.write('contracts', rows)
        self.assertIn('original_purchase_rewritten', self.codes())

    def test_as_of_needs_explicit_offset(self):
        with self.assertRaises(ValueError):
            review(self.after, self.before, ['service'], self.since, self.now.replace(tzinfo=None))

    def test_existing_report_is_never_overwritten(self):
        report = self.root / 'result.json'
        report.write_text('original evidence')
        result = subprocess.run([sys.executable, str(SCRIPT), '--capture', str(self.after), '--baseline', str(self.before), '--contract', 'service', '--since', str(self.since), '--as-of', self.now.isoformat(), '--report', str(report)], capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual('original evidence', report.read_text())


if __name__ == '__main__':
    unittest.main()
