# pylint: disable=invalid-name
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES
from .challenges import init_chals, deinit_chals, define_k8s_admin
from .challenges.k8s_tcp import K8sTcpChallengeType
from .challenges.k8s_web import K8sWebChallengeType
from .challenges.k8s_random_port import K8sRandomPortChallengeType
from .utils import init_db, get_k8s_client, define_k8s_api

def load(app):
    app.db.create_all()
    k8s_client = get_k8s_client()
    print("ctfd-k8s-challenge: Successfully loaded Kubernetes config.")
    init_db()
    define_k8s_admin(app)

    # Run init but don't let it block — we register challenge classes regardless
    try:
        init_chals(k8s_client)
    except Exception as e:
        print(f"ctfd-k8s-challenge: Warning: init_chals failed (non-fatal): {e}")

    # Register challenge types directly — independent of init_chals result
    CHALLENGE_CLASSES['k8s-tcp'] = K8sTcpChallengeType
    CHALLENGE_CLASSES['k8s-web'] = K8sWebChallengeType
    CHALLENGE_CLASSES['k8s-random-port'] = K8sRandomPortChallengeType
    print("ctfd-k8s-challenge: Challenge types registered.")

    register_plugin_assets_directory(app, base_path='/plugins/ctfd-k8s-challenge/assets')
    define_k8s_api(app)
    print("ctfd-k8s-challenge: Plugin loaded successfully.")
