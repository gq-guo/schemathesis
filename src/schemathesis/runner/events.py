import time
from typing import Callable, Iterable, List

import attr
import hypothesis

from ..models import Endpoint, Status, TestResultSet
from ..schemas import BaseSchema


@attr.s()  # pragma: no mutate
class ExecutionEvent:
    """Generic execution event."""

    # Holder for all tests results in a particular run
    results: TestResultSet = attr.ib()  # pragma: no mutate
    # Schema that is being tested
    schema: BaseSchema = attr.ib()  # pragma: no mutate


@attr.s(slots=True)  # pragma: no mutate
class Initialized(ExecutionEvent):
    """Runner is initialized, settings are prepared, requests session is ready."""

    # List of checks that will be used during the run
    checks: Iterable[Callable] = attr.ib()  # pragma: no mutate
    # Settings for `hypothesis` tests
    hypothesis_settings: hypothesis.settings = attr.ib()  # pragma: no mutate
    # Timestamp of test run start
    start_time: float = attr.ib(factory=time.monotonic)


@attr.s(slots=True)  # pragma: no mutate
class BeforeExecution(ExecutionEvent):
    """Happens before each examined endpoint.

    It happens before a single hypothesis test, that may contain many examples inside.
    """

    # Endpoint being tested
    endpoint: Endpoint = attr.ib()  # pragma: no mutate


@attr.s(slots=True)  # pragma: no mutate
class AfterExecution(ExecutionEvent):
    """Happens after each examined endpoint."""

    endpoint: Endpoint = attr.ib()  # pragma: no mutate
    # Endpoint test status - success / failure / error
    status: Status = attr.ib()  # pragma: no mutate
    # Captured hypothesis stdout
    hypothesis_output: List[str] = attr.ib(factory=list)  # pragma: no mutate


@attr.s(slots=True)  # pragma: no mutate
class Interrupted(ExecutionEvent):
    """If execution was interrupted by Ctrl-C or a received SIGTERM."""


@attr.s(slots=True)  # pragma: no mutate
class Finished(ExecutionEvent):
    """The final event of the run.

    No more events after this point.
    """

    # Total test run execution time
    running_time: float = attr.ib()
