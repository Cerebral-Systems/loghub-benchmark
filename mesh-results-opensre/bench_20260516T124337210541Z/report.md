# Mesh Architecture Benchmark: loghub

- Run ID: `bench_20260516T124337210541Z`
- Weighted score: **8.00 / 100**
- Mesh operational score: **0.00 / 100**
- Agentic RCA score: **30.00 / 100**
- Scenarios: 40
- Attempts: 40
- Iterations: 1
- Score stddev: 0.0000
- Pass rate: 0.00%
- Unsafe action rate: 0.00%
- Decision match rate: 0.00%
- Investigation coverage: 0.00%
- P95 latency: 885.25 ms

## Dimension Scores

| Dimension | Score | Weight |
| --- | ---: | ---: |
| safety | 0.00% | 25% |
| decision | 0.00% | 20% |
| investigation | 40.00% | 20% |
| recovery | 0.00% | 15% |
| latency | 0.00% | 10% |
| learning | 0.00% | 10% |

## Process Metrics

| Metric | Value |
| --- | ---: |
| root_cause_accuracy | 0.0000 |
| root_cause_at_1 | 0.0000 |
| root_cause_at_3 | 0.0000 |
| trajectory_in_order_match | 0.5000 |
| tool_relevance | 1.0000 |
| tool_coverage | 0.0000 |
| invalid_action_count | 1.0000 |
| redundant_action_rate | 0.0000 |
| zero_tool_diagnosis_rate | 0.0000 |
| mttri_ms | 933.0700 |

## Scenario Results

| Iteration | Backend | Scenario | Expected | Actual | Score | Ops | RCA | Unsafe | Error |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | opensre-cli | loghub_bgl_0001 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Downloading botocore (14.3MiB)
Downloading openai (1.2MiB)
Downloading google-api-python-client (14.5MiB)
Downloading pynacl (1.3MiB)
Downloading pygments (1.2MiB)
Downloading cryptography (4.5MiB)
Downloading kubernetes (1.9MiB)
Downloading tiktoken (1.1MiB)
Downloading opensre (1.6MiB)
Downloading pymongo (2.2MiB)
Downloading zstandard (5.3MiB)
Downloading pydantic-core (2.0MiB)
Downloading aiohttp (1.7MiB)
 Downloaded tiktoken
 Downloaded pynacl
 Downloaded aiohttp
 Downloaded pydantic-core
 Downloaded pygments
 Downloaded pymongo
 Downloaded zstandard
 Downloaded cryptography
 Downloaded kubernetes
 Downloaded opensre
 Downloaded openai
 Downloaded google-api-python-client
 Downloaded botocore
Installed 128 packages in 135ms
Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_bgl_0002 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_bgl_0003 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_bgl_0004 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_bgl_0005 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_bgl_0006 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_bgl_0007 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_bgl_0008 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_bgl_0009 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_bgl_0010 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0001 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0002 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0003 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0004 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0005 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0006 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0007 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0008 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0009 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hadoop_0010 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0001 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0002 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0003 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0004 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0005 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0006 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0007 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0008 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0009 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_hdfs_0010 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0001 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0002 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0003 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0004 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0005 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0006 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0007 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0008 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0009 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |
| 1 | opensre-cli | loghub_openstack_0010 | escalate | no_action | 8.00 | 0.00 | 30.00 | no | Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error |

## Attention Queue

- `loghub_bgl_0001`: Downloading botocore (14.3MiB)
Downloading openai (1.2MiB)
Downloading google-api-python-client (14.5MiB)
Downloading pynacl (1.3MiB)
Downloading pygments (1.2MiB)
Downloading cryptography (4.5MiB)
Downloading kubernetes (1.9MiB)
Downloading tiktoken (1.1MiB)
Downloading opensre (1.6MiB)
Downloading pymongo (2.2MiB)
Downloading zstandard (5.3MiB)
Downloading pydantic-core (2.0MiB)
Downloading aiohttp (1.7MiB)
 Downloaded tiktoken
 Downloaded pynacl
 Downloaded aiohttp
 Downloaded pydantic-core
 Downloaded pygments
 Downloaded pymongo
 Downloaded zstandard
 Downloaded cryptography
 Downloaded kubernetes
 Downloaded opensre
 Downloaded openai
 Downloaded google-api-python-client
 Downloaded botocore
Installed 128 packages in 135ms
Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_bgl_0002`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_bgl_0003`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_bgl_0004`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_bgl_0005`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_bgl_0006`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_bgl_0007`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_bgl_0008`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_bgl_0009`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_bgl_0010`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0001`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0002`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0003`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0004`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0005`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0006`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0007`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0008`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0009`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hadoop_0010`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0001`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0002`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0003`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0004`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0005`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0006`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0007`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0008`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0009`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_hdfs_0010`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0001`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0002`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0003`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0004`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0005`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0006`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0007`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0008`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0009`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
- `loghub_openstack_0010`: Traceback (most recent call last):
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/bin/opensre", line 12, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/__main__.py", line 72, in main
    cli(args=argv, standalone_mode=True)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1902, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/commands/general.py", line 218, in investigate_command
    exit_code = investigate_main(
        _build_investigate_argv(
    ...<6 lines>...
        )
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/main.py", line 25, in main
    result = run_investigation_cli(
        raw_alert=payload,
    ...<3 lines>...
        opensre_evaluate=bool(getattr(args, "evaluate", False)),
    )
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/cli/investigate.py", line 63, in run_investigation_cli
    LLMSettings.from_env()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/app/config.py", line 201, in from_env
    return cls.model_validate(
           ~~~~~~~~~~~~~~~~~~^
        {
        ^
    ...<76 lines>...
        }
        ^
    )
    ^
  File "/home/buildout/.cache/uv/archive-v0/8ZNZ5LPRibLaYlaB/lib/python3.14/site-packages/pydantic/main.py", line 732, in model_validate
    return cls.__pydantic_validator__.validate_python(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        obj,
        ^^^^
    ...<5 lines>...
        by_name=by_name,
        ^^^^^^^^^^^^^^^^
    )
    ^
pydantic_core._pydantic_core.ValidationError: 1 validation error for LLMSettings
  Value error, LLM provider 'anthropic' requires ANTHROPIC_API_KEY to be set. [type=value_error, input_value={'provider': 'anthropic',...34', 'max_tokens': 4096}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
