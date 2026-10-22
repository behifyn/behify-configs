import importlib.util
import json
import pathlib
import unittest

MODULE_FILE = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'import_experimental.py'
spec = importlib.util.spec_from_file_location('import_experimental', MODULE_FILE)
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)


class ImportExperimentalTest(unittest.TestCase):
    def test_jsonc_preserves_slashes_in_strings(self):
        source = '{"endpoint":"https://dns.example/dns-query", // trailing comment\n"labels":["x,//y",], /* block */ "port":10808,}'
        parsed = json.loads(importer.strip_jsonc(source))
        self.assertEqual(parsed['endpoint'], 'https://dns.example/dns-query')
        self.assertEqual(parsed['labels'], ['x,//y'])
        self.assertEqual(parsed['port'], 10808)

    def test_adapt_limits_network_listen_and_preserves_outbound(self):
        config = {
            '__Credits__': {'creator': 'origin'},
            'remarks': 'Source',
            'log': {'loglevel': 'debug', 'dnsLog': True},
            'inbounds': [{'tag': 'local', 'port': 10808, 'protocol': 'mixed'}],
            'outbounds': [{'tag': 'direct', 'protocol': 'direct'}],
        }
        output = importer.adapt(json.dumps(config).encode(), 'Behify test')
        self.assertEqual(output['inbounds'][0]['listen'], '127.0.0.1')
        self.assertNotIn('__Credits__', output)
        self.assertEqual(output['remarks'], 'Behify test')
        self.assertEqual(output['log']['loglevel'], 'warning')
        self.assertEqual(output['log']['dnsLog'], False)
        self.assertEqual(output['outbounds'], config['outbounds'])

    def test_adapt_rejects_public_inbound(self):
        config = {
            'inbounds': [{'listen': '0.0.0.0', 'port': 10808}],
            'outbounds': [{'tag': 'direct', 'protocol': 'direct'}],
        }
        with self.assertRaisesRegex(ValueError, 'non-loopback'):
            importer.adapt(json.dumps(config).encode(), 'Test')

    def test_invalid_unterminated_block_comment(self):
        with self.assertRaisesRegex(ValueError, 'Unterminated'):
            importer.strip_jsonc('{"hello":1 /* oops')


if __name__ == '__main__':
    unittest.main()
