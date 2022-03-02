# lemur-cloudwatch

[Cloudwatch](https://aws.amazon.com/fr/cloudwatch/) metric plugin for [Lemur](https://github.com/netflix/lemur).

## Installation

```
pip install -e git+https://github.com/railnova/lemur-cloudwatch#egg=lemur-cloudwatch
```

## Configuration

Add the following to your `lemur.conf.py`:

```python
# Add to active metric providers
METRIC_PROVIDERS = ['cloudwatch']

# Set the following variables
CLOUDWATCH_AWS_ACCESS_KEY_ID = "..."
CLOUDWATCH_AWS_SECRET_ACCESS_KEY = "..."
CLOUDWATCH_AWS_REGION = "..."
CLOUDWATCH_AWS_NAMESPACE = "..."
```
