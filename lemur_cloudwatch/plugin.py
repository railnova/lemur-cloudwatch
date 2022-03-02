"""
.. module: lemur.plugins.lemur_cloudwatch.plugin
    :platform: Unix
    :copyright: (c) 2021 by Railnova, see AUTHORS for more
    :license: MIT, see LICENSE for more details.

.. moduleauthor:: Nicolas Surleraux <nicolas.surleraux@railnova.eu>
"""
from datetime import datetime

import boto3
from flask import current_app
from lemur.plugins.bases.metric import MetricPlugin


def metrics_tags_to_dimensions(metrics_tags):
    dims = []
    for k, v in metrics_tags:
        dims.append({
            'Name': k,
            'Value': v
        })
    return dims


def metric_type_to_cloudwatch_unit(metric_type):
    if metric_type == 'counter':
        return 'Count'

    current_app.logger.warning(f"Got unhandled metric_type: {metric_type}, returning Count anyway.")
    return 'Count'


class CloudwatchMetricPlugin(MetricPlugin):
    title = 'Cloudwatch'
    slug = 'cloudwatch'
    description = 'Adds support for sending key metrics to Cloudwatch'
    version = '1.0.0'

    author = 'Nicolas Surleraux'
    author_url = 'https://github.com/railnova/lemur-cloudwatch'

    def __init__(self, *args, **kwargs):
        cfg = current_app.config
        access_key_id = cfg.get('CLOUDWATCH_AWS_ACCESS_KEY_ID', None)
        secret_key = cfg.get('CLOUDWATCH_AWS_SECRET_ACCESS_KEY', None)
        region = cfg.get('CLOUDWATCH_AWS_REGION', None)
        self.namespace = cfg.get('CLOUDWATCH_AWS_NAMESPACE', None)
        assert access_key_id is not None
        assert secret_key is not None
        assert region is not None
        assert self.namespace is not None

        self.client = boto3.client(
            'cloudwatch',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        super(CloudwatchMetricPlugin, self).__init__(*args, **kwargs)

    def submit(self, metric_name, metric_type, metric_value, metric_tags=None, options=None):
        if not options:
            options = self.options

        current_app.logger.info("InfluxDB ignores metric types (got '%s')",
                                metric_type)

        if not metric_tags:
            metric_tags = {}

        if not isinstance(metric_tags, dict):
            raise Exception(
                "Invalid Metric Tags for InfluxDB: Tags must be in dict format"
            )

        self.client.put_metric_data(
            Namespace=self.namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': metrics_tags_to_dimensions(metric_tags),
                    'Value': metric_value,
                    'Timestamp': datetime.now(),
                    'Unit': metric_type_to_cloudwatch_unit(metric_type)
                },
            ]
        )

