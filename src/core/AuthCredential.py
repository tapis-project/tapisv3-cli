class AuthCredential:
    def __init__(
        self,
        password=None,
        public_key=None,
        private_key=None
    ):
        self.password = password
        self.public_key = public_key
        self.private_key = private_key