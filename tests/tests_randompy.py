from randompy import RandomMockAPI, RandomPy


class RandomPyMock(RandomPy):

    def __init__(self, signed=True):
        self.config = self._get_config()
        self.key = 'mockkey'
        self.signed = signed
        self.fmt = 'Signed' if signed else ''
        self.api = RandomMockAPI('url')


class TestGenerateUnsigned:

    def setup(self):
        self.r = RandomPyMock(signed=False)

    def teardown(self):
        self.r = None

    def returnfunc(self, resp):
        return resp

    def test_integers_n(self):
        f = self.returnfunc
        req = self.r.integers(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_integers_method(self):
        f = self.returnfunc
        req = self.r.integers(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateIntegers'

    def test_decimals_n(self):
        f = self.returnfunc
        req = self.r.decimals(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_decimals_method(self):
        f = self.returnfunc
        req = self.r.decimals(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateDecimalFractions'

    def test_gaussians_n(self):
        f = self.returnfunc
        req = self.r.gaussians(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_gaussians_method(self):
        f = self.returnfunc
        req = self.r.gaussians(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateGaussians'

    def test_strings_n(self):
        f = self.returnfunc
        req = self.r.strings(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_strings_method(self):
        f = self.returnfunc
        req = self.r.strings(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateStrings'

    def test_uuids_n(self):
        f = self.returnfunc
        req = self.r.uuids(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_uuids_method(self):
        f = self.returnfunc
        req = self.r.uuids(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateUUIDs'

    def test_blobs_n(self):
        f = self.returnfunc
        req = self.r.blobs(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_blobs_method(self):
        f = self.returnfunc
        req = self.r.blobs(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateBlobs'


class TestGenerateSigned:

    def setup(self):
        self.r = RandomPyMock()

        def verify(*args):
            return True

        self.r._verify_response = verify

    def teardown(self):
        self.r = None

    def returnfunc(self, resp):
        return resp

    def test_integers_n(self):
        f = self.returnfunc
        req = self.r.integers(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_integers_method(self):
        f = self.returnfunc
        req = self.r.integers(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateSignedIntegers'

    def test_decimals_n(self):
        f = self.returnfunc
        req = self.r.decimals(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_decimals_method(self):
        f = self.returnfunc
        req = self.r.decimals(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateSignedDecimalFractions'

    def test_gaussians_n(self):
        f = self.returnfunc
        req = self.r.gaussians(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_gaussians_method(self):
        f = self.returnfunc
        req = self.r.gaussians(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateSignedGaussians'

    def test_strings_n(self):
        f = self.returnfunc
        req = self.r.strings(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_strings_method(self):
        f = self.returnfunc
        req = self.r.strings(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateSignedStrings'

    def test_uuids_n(self):
        f = self.returnfunc
        req = self.r.uuids(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_uuids_method(self):
        f = self.returnfunc
        req = self.r.uuids(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateSignedUUIDs'

    def test_blobs_n(self):
        f = self.returnfunc
        req = self.r.blobs(4, errorfunc=f, successfunc=f)
        assert req['params']['n'] == 4

    def test_blobs_method(self):
        f = self.returnfunc
        req = self.r.blobs(4, errorfunc=f, successfunc=f)
        assert req['method'] == 'generateSignedBlobs'
