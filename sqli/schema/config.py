import trafaret as T


CONFIG_SCHEMA = T.Dict({
    T.Key('db'): T.Dict({
        'user': T.String(),
        'password': T.String(),
        'host': T.String(),
        'port': T.Int(),
        'database': T.String(),
    }),
    T.Key('redis'): T.Dict({
        'host': T.String(),
        'port': T.Int(),
        'db': T.Int(),
    }),
    T.Key('environment'): T.String(),
    T.Key('development', default={}): T.Dict({
        T.Key('session_cookie', optional=True): T.Dict({
            'secure': T.Bool(),
            'httponly': T.Bool(),
        }),
    }),
    T.Key('app'): T.Dict({
        'secret': T.String(),
        T.Key('debug', default=True): T.Bool(),
        'host': T.String(),
        'port': T.Int(),
    }),
})
