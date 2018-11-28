#!/usr/bin/env bash

function get_app_guid {
  local ORG=$(awk -F/ '{print $1}' <<< $@)
  local SPACE=$(awk -F/ '{print $2}' <<< $@)
  local APP=$(awk -F/ '{print $3}' <<< $@)
  cf target -o $ORG -s $SPACE 2>&1 > /dev/null
  cf app $APP --guid
}

function main {
  SRC_GUID=$(get_app_guid $1)
  DEST_GUID=$(get_app_guid $2)
  DEST_APP_PORT=$(cf curl "/v2/apps/$DEST_GUID" | jq -rC '.entity.ports[]')
  cf curl "/networking/v1/external/policies" -X POST -d '{
    "policies": [
      {
        "source": {
          "id": "'$SRC_GUID'"
        },
        "destination": {
          "id": "'$DEST_GUID'",
          "protocol": "tcp",
          "ports": {
            "start": '$DEST_APP_PORT',
            "end": '$DEST_APP_PORT'
          }
        }
      }
    ]
  }'
}

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 [source_app|org/space/app] [destination_app|org/space/app]"
  exit 255
fi
main "$@"
