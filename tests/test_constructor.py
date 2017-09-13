import sys
import pytest

from tpl.constructor import construct_context_from_py
from candy.utils.faker import *
from candy.path.temp import TempFile


def test_construct_context_from_py():
    with TempFile(random_lower_string(), 'py') as f:
        f.fd.write('def construct():return {"key":"value"}')
        f.fd.flush()
        context = construct_context_from_py(f.path)
        assert isinstance(context, dict)
        assert context.get('key') == 'value'

    sys.path_importer_cache.clear()

    with TempFile(random_lower_string(), 'py') as f:
        f.fd.write(random_lower_string())
        f.fd.flush()
        with pytest.raises(NameError):
            construct_context_from_py(f.path)

    sys.path_importer_cache.clear()

    with TempFile(random_lower_string(), 'py') as f:
        f.fd.write('def construct():return None')
        f.fd.flush()
        context = construct_context_from_py(f.path)
        assert context is None

