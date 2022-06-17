#!/bin/bash

if [ "$_" = "$0" ]; then
    echo -e "\e[1;31m!!!   The script must be run via the source(.) command. e.g.: '. $0'  !!!\e[0m"
    exit 1
fi

DEBUG=false

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Input args
if [ -n "$1" ]; then
    TAG_ID=$1  
else
    TAG_ID="android-automotive"
fi

# AOSP build vars
HOST_OUT=$(get_build_var "HOST_OUT")
TARGET_PRODUCT=$(get_build_var "TARGET_PRODUCT")
PRODUCT_MANUFACTURER=$(get_build_var "PRODUCT_MANUFACTURER")
PRODUCT_MODEL=$(get_build_var "PRODUCT_MODEL")
PLATFORM_SDK_VERSION=$(get_build_var "PLATFORM_SDK_VERSION")
TARGET_ARCH=$(get_build_var "TARGET_ARCH")

SDK_ARCHIVE=$(find "$ANDROID_BUILD_TOP/$HOST_OUT/sdk/$TARGET_PRODUCT" -name "android-sdk*.zip")

if $DEBUG; then
    # AOSP build vars
    echo "HOST_OUT:             $HOST_OUT"
    echo "TARGET_PRODUCT:       $TARGET_PRODUCT"
    echo "PRODUCT_MANUFACTURE:  $PRODUCT_MANUFACTURER"
    echo "PRODUCT_MODEL:        $PRODUCT_MODEL"
    echo "PLATFORM_SDK_VERSION: $PLATFORM_SDK_VERSION"
    echo "TARGET_ARCH:          $TARGET_ARCH"
    # AOSP env vars
    echo "ANDROID_BUILD_TOP:    $ANDROID_BUILD_TOP"
    # My
    echo "SDK_ARCHIVE:          $SDK_ARCHIVE"
fi

python $SCRIPT_PATH/sys-img-xml-builder.py \
    --sdk_archive  "$SDK_ARCHIVE" \
    --template_xml "$SCRIPT_PATH/../templates/sys-img-template.xml" \
    --platform_sdk_version "$PLATFORM_SDK_VERSION" \
    --target_arch "$TARGET_ARCH" \
    --product_manufacturer "$PRODUCT_MANUFACTURER" \
    --product_model "$PRODUCT_MODEL" \
    --tag_id "$TAG_ID"