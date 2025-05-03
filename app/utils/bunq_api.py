from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq import ApiEnvironmentType

import os


def init_api_context():
    api_context = ApiContext.create(
        ApiEnvironmentType.SANDBOX,  # SANDBOX for testing
        os.getenv("BUNQ_API_KEY"),
        "My Agent",
    )
    api_context.save("bunq_api_context.conf")

    BunqContext.load_api_context(api_context)

