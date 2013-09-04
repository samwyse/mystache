'''Run tests from a semanticly versioned specification.'''

import json, requests, unittest


class SVTestCase(unittest.TestCase):

    def __init__(self, test, func, section=''):
        unittest.TestCase.__init__(self)
        self._func = func
        self._name = test.pop('name')
        if section:
            self._name = '%s: %s' % (section.title(), self._name) 
        self._desc = test.pop('desc', '')
        self._expected = test.pop('expected')
        # Setting '_keywords' must be the last thing done with spec.
        self._args = test.pop('args', ())
        self._keywords = test.pop('keywords', test)

    def runTest(self):
        expected_result = self._expected
        actual_result = self._func(*self._args, **self._keywords)
        self.assertEqual(expected_result, actual_result)

    def id(self):
        return '%s: %s' % self._name

    __str__ = id

    def __repr__(self):
        return 'SVTestCase(%s, %s)' % (str(self), repr(self.runTest.func))

    def shortDescription(self):
        return self._desc


class PystacheTestCase(SVTestCase):
    '''Adapter for Pystache'''

    def runTest(self):
        '''Instantiate a renderer, and render with it.'''
        expected_result = self._expected
        partials = self._keywords.get('partials', {})
        template = self._keywords.get('template', '')
        data = self._keywords.get('data', {})
        actual_result = self._func(partials=partials).render(template, data)
        self.assertEqual(expected_result, actual_result)


def spec_suite(name, func, TestCase=SVTestCase,
               url='https://raw.github.com/mustache/spec/master/specs/%s.json'):
    '''Create a suite of semantically versioned tests.'''
    spec = json.loads(requests.get(url % name).content)
    return unittest.TestSuite(TestCase(test, func, name)
                              for test in spec['tests'])

def test_pystache(spec_names):
    import pystache

    renderer = pystache.Renderer
    tests = unittest.TestSuite(spec_suite(name, renderer, TestCase=PystacheTestCase)
                               for name in spec_names)
    unittest.runner.TextTestRunner().run(tests)

all_specs = set('comments delimiters interpolation inverted partials sections ~lambdas'.split())
base_specs = set(item for item in all_specs if not item.startswith('~'))
advanced_specs = all_specs.difference(base_specs)

if __name__ == '__main__':
    test_pystache(base_specs)
