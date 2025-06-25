import pytest
from typing import *
from base_aux.servers.m0_url import Url
from base_aux.lambdas.m1_lambda import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="kwargs_source, kwargs_resolve, _EXPECTED",
    argvalues=[
        (dict(), dict(), "http://localhost:80/"),

        (dict(host="host"), dict(), "http://host:80/"),

        (dict(host="host", route="route"), dict(), "http://host:80/route"),

        (dict(host="host", route="route"), dict(host="host2"), "http://host2:80/route"),

        (dict(host="host", route="route"), dict(port=8080), "http://host:8080/route"),

        # ROUTE ---
        (dict(host="host", route="route"), dict(route=""), "http://host:80/"),
        (dict(host="host", route="route"), dict(route="route2"), "http://host:80/route2"),
        (dict(host="host", route="route"), dict(route="/route2"), "http://host:80/route2"),
        (dict(host="host", route="route"), dict(route="//route2"), "http://host:80/route2"),
        (dict(host="host", route="route"), dict(route="///route2"), "http://host:80/route2"),

        (dict(host="host", route="route"), dict(route="route2/"), "http://host:80/route2/"),
        (dict(host="host", route="route"), dict(route="route2///"), "http://host:80/route2///"),

        (dict(host="host", route="route"), dict(route="route2/3"), "http://host:80/route2/3"),
        (dict(host="host", route="route"), dict(route="2/3"), "http://host:80/2/3"),
        (dict(host="host", route="route"), dict(route=(2, 3)), "http://host:80/2/3"),
        (dict(host="host", route="route"), dict(route=[2, 3]), "http://host:80/2/3"),
        (dict(host="host", route="route"), dict(route=[]), "http://host:80/"),

    ]
)
def test__url(kwargs_source, kwargs_resolve, _EXPECTED):
    Lambda(Url(**kwargs_source).resolve, **kwargs_resolve).expect__check_assert(_EXPECTED)


# =====================================================================================================================
