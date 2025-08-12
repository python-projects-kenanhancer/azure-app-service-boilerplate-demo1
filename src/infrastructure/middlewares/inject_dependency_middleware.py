import inspect

from ..decorators.pipeline_decorator import Context, Next


def inject_dependency_middleware(context: Context, next: Next):

    func = context.func
    original_args = context.args
    original_kwargs = dict(context.kwargs)  # make a copy so we can modify safely

    sig = inspect.signature(func)
    param_names = set(sig.parameters.keys())

    # Grab the injector object if any (from container_builder_middleware)
    injector_obj = original_kwargs.get("injector", None)

    # If the function does NOT declare **kwargs, remove unrecognized keys
    # so that bind_partial won't complain about an extra param.
    has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())

    if not has_var_keyword:
        # Filter out all kwargs that are not in param_names
        original_kwargs = {k: v for k, v in original_kwargs.items() if k in param_names}

    # Now bind partial with the safe set of kwargs
    bound_args = sig.bind_partial(*original_args, **original_kwargs)
    bound_args.apply_defaults()

    # For each unfilled parameter with a type annotation, attempt injection
    for param_name, param in sig.parameters.items():
        if param_name not in bound_args.arguments:
            annotated_type = param.annotation

            # If the param is typed, we try to get it from 'injector_obj'
            if annotated_type != inspect.Parameter.empty:
                if injector_obj is None:
                    # No injector found - user can decide to raise or skip
                    raise RuntimeError(
                        f"Cannot inject '{param_name}' (type={annotated_type}) "
                        f"because no injector is available. "
                        "Did you forget to add container_builder_middleware?"
                    )
                # Attempt to resolve from the injector
                dependency = injector_obj.get(annotated_type)
                bound_args.arguments[param_name] = dependency

    # Update context with the newly bound arguments
    context.args = bound_args.args
    # The right-side dict takes precedence, so existing context kwargs take precedence
    context.kwargs = bound_args.kwargs | context.kwargs

    return next()
