#!/bin/bash

# Configuration
AWS_ACCESS_KEY="test"
AWS_SECRET_KEY="testtest"
REGION="fr-gre-0"
BUCKET="test"
OBJECT_KEY="coucou.txt"
FILE_PATH="./coucou.txt"
SERVICE="s3"
HOST="localhost:9000"
#CONTENT_TYPE="text/plain"
DATE=$(date -u "+%Y%m%dT%H%M%SZ")
SHORT_DATE=$(date -u "+%Y%m%d")

# Create Canonical Request
REQUEST_PAYLOAD=$(cat "${FILE_PATH}")
HASHED_PAYLOAD=$( printf "${REQUEST_PAYLOAD}" | openssl dgst -binary -sha256 | xxd -p -c 256 )
echo HASHED_PAYLOAD : ${HASHED_PAYLOAD}

CANONICAL_HEADERS="host:${HOST}\nx-amz-content-sha256:${HASHED_PAYLOAD}\nx-amz-date:${DATE}"
SIGNED_HEADERS="host;x-amz-content-sha256;x-amz-date"

CANONICAL_REQUEST=$( printf "PUT
/
${BUCKET}/${OBJECT_KEY}
${CANONICAL_HEADERS}
${SIGNED_HEADERS}
${HASHED_PAYLOAD}" )

echo "DEBUG: canonical request: ${CANONICAL_REQUEST}"

HASHED_CANONICAL_REQUEST=$( printf "${CANONICAL_REQUEST}" | openssl dgst -binary -sha256 | xxd -p -c 256 )


# Create String to Sign
ALGORITHM="AWS4-HMAC-SHA256"
CREDENTIAL_SCOPE="$SHORT_DATE/$REGION/$SERVICE/aws4_request"

#STRING_TO_SIGN="$ALGORITHM\n$DATE\n$CREDENTIAL_SCOPE\n$HASHED_CANONICAL_REQUEST"

STRING_TO_SIGN=$( printf "${ALGORITHM}
${DATE}
${CREDENTIAL_SCOPE}
${HASHED_CANONICAL_REQUEST}" )
echo "DEBUG: stringToSign: ${STRING_TO_SIGN}"


# Create Signing Key
kSecret=$(printf "AWS4${AWS_SECRET_KEY}" | xxd -p -c 256 )
kDate=$(printf "${SHORT_DATE}" | openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:${kSecret} | xxd -p -c 256 )
kRegion=$(printf "${REGION}" | openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:${kDate} | xxd -p -c 256 )
kService=$(printf "${SERVICE}" | openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:${kRegion} | xxd -p -c 256 )
kSigning=$(printf "aws4_request" | openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:${kService} | xxd -p -c 256 )
SIGNATURE=$(printf "${STRING_TO_SIGN}" | openssl dgst -binary -hex -sha256 -mac HMAC -macopt hexkey:${kSigning} | sed 's/^.* //' )

# Generate Signature
SIGNATURE=$( printf "${STRING_TO_SIGN}"  | openssl dgst -binary -hex -sha256 -mac HMAC -macopt hexkey:${kSigning} | sed 's/^.* //' )
echo signature: $SIGNATURE

# Build Authorization Header
AUTH_HEADER="$ALGORITHM Credential=$AWS_ACCESS_KEY/$CREDENTIAL_SCOPE, SignedHeaders=$SIGNED_HEADERS, Signature=$SIGNATURE"

# Upload using curl
curl -v -X PUT "http://$HOST/$BUCKET/$OBJECT_KEY" \
  -H "Host: $HOST" \
  -H "x-amz-content-sha256: $HASHED_PAYLOAD" \
  -H "x-amz-date: $DATE" \
  -H "Authorization: $AUTH_HEADER" \
  --upload-file "$FILE_PATH"
