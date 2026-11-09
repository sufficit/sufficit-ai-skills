#!/usr/bin/env python3
"""Read one explicitly provisioned QuePasa session; never pair, send or mutate it."""
import argparse
import datetime
import json
import os
import subprocess
import urllib.parse
from pathlib import Path
import urllib.error
import urllib.request

HEALTH_FIELDS = {'success', 'status', 'timestamp', 'wid', 'state', 'state_code', 'servingHost', 'runtimeHost', 'runtimeState', 'runtimeStale', 'runtimeObservedAt', 'runtimeLeaseExpiresAt'}
SESSION_FIELDS = {'id', 'wid', 'contextid', 'state', 'calls', 'calls_effective', 'calls_policy', 'voipmode', 'voip_mode', 'manually_stopped', 'sip_register_enabled', 'host', 'assignedHost', 'runtimeState', 'runtimeStale', 'runtimeObservedAt', 'runtimeLeaseExpiresAt'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phone')
    parser.add_argument('--config', default=os.environ.get('QUEPASA_SESSION_DIAGNOSTIC_CONFIG', '/data/support/quepasa-readonly/config.json'))
    args = parser.parse_args()
    try:
        config = json.loads(Path(args.config).read_text())
        phone = ''.join(c for c in args.phone if c.isascii() and c.isdigit())
        if phone not in config['phones']:
            print(json.dumps({'error': 'number_not_in_provisioned_scope'}))
            return 2
        base = config['baseUrl'].rstrip('/')
        if base != 'https://quepasa.sufficit.com.br':
            raise ValueError('unexpected gateway')
        token = Path(config['tokenFile']).read_text().strip()
        if not token:
            raise ValueError('missing credential')
        result = {'queriedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'phone': phone, 'sessionId': config['sessionId'], 'checks': {}}
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        opener = urllib.request.build_opener(NoRedirect())
        for name, path, body, fields in [('health', '/api/v5/health', None, HEALTH_FIELDS), ('session', '/api/v5/sessions/get', b'{}', SESSION_FIELDS)]:
            req = urllib.request.Request(base + path, data=body, headers={'X-QUEPASA-TOKEN': token, 'Content-Type': 'application/json'})
            try:
                with opener.open(req, timeout=25) as response:
                    value = json.load(response)
                    if name == 'session':
                        selected = value.get('session') or value.get('server') or {}
                    else:
                        selected = value
                    wid_phone = str(selected.get('wid', '')).split(':')[0].split('@')[0]
                    if (selected.get('id') and selected['id'] != config['sessionId']) or (wid_phone and wid_phone not in config['phones']):
                        result['checks'][name] = {'error': 'session_scope_mismatch'}
                        continue
                    result['checks'][name] = {'httpStatus': response.status, 'data': {k: v for k, v in selected.items() if k in fields}}
            except urllib.error.HTTPError as error:
                result['checks'][name] = {'httpStatus': error.code, 'error': 'gateway_rejected_query'}
            except (OSError, ValueError):
                result['checks'][name] = {'error': 'gateway_query_failed'}
        context = config.get('sufficitContextId')
        if context:
            def api(path):
                call = subprocess.run(['dotnet', '/data/support/api-client/api-helper.dll', 'endpoints', 'GET', path], capture_output=True, text=True, timeout=65)
                value = json.loads(call.stdout)
                return value['status'], value.get('data')
            try:
                status, routes = api('/Gateway/WhatsApp/context/' + context)
                matches = [r for r in (routes or []) if isinstance(r, dict) and (r.get('token') == token or r.get('sessionId', r.get('sessionid')) == token or ''.join(c for c in str(r.get('phone', '')) if c.isdigit()) in config['phones'])] if status == 200 else []
                fields = {'contextId', 'contextid', 'phone', 'enabled', 'mode', 'callMode', 'destinationAsterisk', 'destinationasterisk', 'description'}
                result['checks']['gatewayRoutes'] = {'httpStatus': status, 'contextId': context, 'matches': [{k: v for k, v in r.items() if k in fields} for r in matches]}
                if len(matches) == 1:
                    route_id = matches[0].get('sessionId', matches[0].get('sessionid'))
                    if route_id:
                        status, report = api('/Gateway/WhatsApp/diagnostics?sessionid=' + urllib.parse.quote(route_id, safe=''))
                        safe_fields = {'provider', 'phone', 'enabled', 'destination', 'connectionState', 'summary', 'diagnosedAt', 'contextId', 'contextid'}
                        selected = {k: v for k, v in (report or {}).items() if k in safe_fields} if isinstance(report, dict) else {}
                        selected['items'] = [{k: v for k, v in item.items() if k in {'id', 'title', 'description', 'severity', 'critical'}} for item in report.get('items', [])] if isinstance(report, dict) else []
                        result['checks']['gatewayDiagnostics'] = {'httpStatus': status, 'data': selected}
            except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
                result['checks']['gatewayRoutes'] = {'error': 'gateway_route_query_failed'}
        # Whitelisting prevents raw credential fields and unrelated session data from escaping.
        print(json.dumps(result, ensure_ascii=False).replace(token, '[redacted]'))
        return 0
    except (OSError, ValueError, KeyError):
        print(json.dumps({'error': 'diagnostic_scope_or_credential_unavailable'}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
