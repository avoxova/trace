"""Offline regression tests; RPC responses are test fixtures, not chain evidence."""
import json
import types
import unittest
from pathlib import Path
from unittest.mock import Mock
import verify


class HistoricalBalanceTests(unittest.TestCase):
    def test_rate_limit_is_not_reported_as_missing_archive(self):
        claims = json.loads(Path('claims.json').read_text(encoding='utf-8'))
        for key in ('bsc_transfers', 'bsc_approvals', 'bsc_balances_now', 'xrp_payments'):
            claims[key] = []
        claims['xrpscan_labels'] = {}
        claims['cobo']['deposits'] = []
        claims['cobo']['tag_totals'] = {}
        reason = "eth_call: {'code': -32005, 'message': 'You have reached the maximum API usage limit'}"
        chain = Mock()
        chain.eth.side_effect = RuntimeError(reason)
        verify.ARGS = types.SimpleNamespace(json=True)
        report = verify.Report()
        verify.run(claims, chain, report)
        row = next(r for r in report.rows if r['id'] == 'collection_balance')
        self.assertEqual(row['status'], 'SKIP')
        self.assertIn(reason, row['detail'])
        self.assertNotIn('needs an archive BSC node', row['detail'])
        self.assertIn('not verified', row['detail'])


if __name__ == '__main__':
    unittest.main()
