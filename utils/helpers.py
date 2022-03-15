import logging

def get_or_create_pipeline(client,
                    pipeline_name: str, 
                    pipeline_description: str, 
                    version: str
                   ):
    pipeline_package_path = f"pipeline_{version}.yaml"
    pipeline_id = client.get_pipeline_id(pipeline_name)

    # If no pipeline found by name, create a new pipeline
    # Else get the latest pipeline version
    if pipeline_id is None:
        logging.info(f"Creating a new pipeline: {pipeline_name}")
        pipeline = client.upload_pipeline(
            pipeline_package_path=pipeline_package_path,
            pipeline_name=pipeline_name,
            description=pipeline_description
        )
    else:
        pipeline = client.get_pipeline(pipeline_id)

    # Always try to upload a pipeline version.
    pipeline_version = client.upload_pipeline_version(
        pipeline_package_path=pipeline_package_path,
        pipeline_version_name=f"{pipeline_name} {version}",
        pipeline_id=pipeline_id
    )

    return pipeline_version


def get_or_create_experiment(client, 
                      name: str
                     ):
    try:
        experiment = client.get_experiment(
            experiment_name=name
        )
    except Exception:
        logging.info(f"Creating new experiment: {name}")
        experiment = client.create_experiment(name)

    return experiment
