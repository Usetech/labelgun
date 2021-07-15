# Запускает прогон тестов в github actions
DOCKER_IMAGE=registry.usetech.ru/pub/labelgun/ci:${GITHUB_REF:11}
VOLUME_SOURCE=/home/runner/work/labelgun/labelgun
VOLUME_TARGET=/opt/app
COVERAGE_TARGET=./labelgun
MIN_COVERAGE=96

docker run \
          --rm \
          --volume $VOLUME_SOURCE:$VOLUME_TARGET $DOCKER_IMAGE \
          bash -c "
                  pytest \
                        --cov=$COVERAGE_TARGET \
                        --cov-report html:coverage \
                        --cov-fail-under=$MIN_COVERAGE \
                        --html test-report.html \
                        --showlocals \
                        -v \
                        ."
