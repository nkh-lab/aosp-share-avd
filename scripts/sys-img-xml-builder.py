import argparse
import sys
import os
import hashlib


class SysImgXmlBuilder:
    # Define some properties which are used in the code
    PROP_SDK_ARCHIVE = "sdk_archive"
    PROP_TEMPLATE_XML = "template_xml"
    PROP_OUTPUT_XML = "output_xml"
    PROP_SDK_ARCHIVE_SIZE = "sdk_archive_size"
    PROP_SDK_ARCHIVE_CHECKSUM = "sdk_archive_checksum"
    PROP_SDK_ARCHIVE_FILENAME = "sdk_archive_filename"
    PRODUCT_MANUFACTURER = "product_manufacturer"

    COLUMN_IDX_NAME = 0
    COLUMN_IDX_VALUE = 3

    props = [
        #
        # Name                      cfg     xml     Value
        #
        [PROP_SDK_ARCHIVE,          True,   False,  None],
        [PROP_TEMPLATE_XML,         True,   False,  None],
        [PROP_OUTPUT_XML,           True,   False,  ""],

        ["license",                 True,   True,   "Some license text"],
        ["platform_sdk_version",    True,   True,   None],  # 32
        ["target_arch",             True,   True,   None],  # armeabi-v7a, x86
        [PRODUCT_MANUFACTURER,      True,   True,   None],  # lower case, no spaces
        ["product_model",           True,   True,   None],
        # android-automotive, android-tv
        ["tag_id",                  True,   True,   None],
        ["package_revision_major",  True,   True,   1],
        ["package_revision_minor",  True,   True,   0],
        [PROP_SDK_ARCHIVE_SIZE,     False,  True,   None],
        [PROP_SDK_ARCHIVE_CHECKSUM, False,  True,   None],
        [PROP_SDK_ARCHIVE_FILENAME, False,  True,   None],
    ]

    def get_cfg_prop_names(self):
        return [name for name, cfg, xml, value in self.props if cfg is True]

    def get_none_cfg_prop_names(self):
        return [name for name, cfg, xml, value in self.props if cfg is True and value is None]

    def get_xml_prop_names(self):
        return [name for name, cfg, xml, value in self.props if xml is True]

    def set_prop_value(self, prop_name, prop_value):
        for i, row in enumerate(self.props):
            if row[self.COLUMN_IDX_NAME] == prop_name:
                row[self.COLUMN_IDX_VALUE] = prop_value
                break

    def get_prop_value(self, prop_name):
        for i, row in enumerate(self.props):
            if row[self.COLUMN_IDX_NAME] == prop_name:
                return row[self.COLUMN_IDX_VALUE]
        return None

    def build(self):
        if self._build_props():
            self._build_xml()
            return True
        else:
            return False

    def _replace_pattern(self, line):
        new_line = line
        for prop in self.get_xml_prop_names():
            pattern = "{{" + "".join(prop).upper() + "}}"
            value = self.get_prop_value(prop)
            if value is not None:
                new_line = str.replace(new_line, pattern, str(value))
        return new_line

    def _calc_file_size(self, file):
        return os.path.getsize(file)

    def _calc_file_checksum(self, file):
        sha1 = hashlib.sha1()
        with open(file, "rb") as source:
            block = source.read(2**16)
            while len(block) != 0:
                sha1.update(block)
                block = source.read(2**16)
        return sha1.hexdigest()

    def _build_props(self):
        ret = True

        sdk_archive_path = self.get_prop_value(self.PROP_SDK_ARCHIVE)

        if os.path.exists(sdk_archive_path):
            if self.get_prop_value(self.PROP_OUTPUT_XML) == "":
                output_xml = ".xml".join(sdk_archive_path.rsplit(".zip", 1))
                self.set_prop_value(self.PROP_OUTPUT_XML, output_xml)

            file_path, file_name = os.path.split(sdk_archive_path)
            self.set_prop_value(self.PROP_SDK_ARCHIVE_FILENAME, file_name)
            self.set_prop_value(self.PROP_SDK_ARCHIVE_SIZE,
                                self._calc_file_size(sdk_archive_path))
            self.set_prop_value(self.PROP_SDK_ARCHIVE_CHECKSUM,
                                self._calc_file_checksum(sdk_archive_path))

            product_manufacturer = self.get_prop_value(
                self.PRODUCT_MANUFACTURER)
            product_manufacturer.lower().replace(" ", "_")
            self.set_prop_value(self.PRODUCT_MANUFACTURER,
                                product_manufacturer)

        else:
            print("Error: file doesn't exist: " + sdk_archive_path)
            ret = False

        return ret

    def _build_xml(self):
        out = ""
        with open(self.get_prop_value(self.PROP_TEMPLATE_XML)) as t:
            for line in t.readlines():
                out += self._replace_pattern(line)
        # Debug
        # print(out)

        with open(self.get_prop_value(self.PROP_OUTPUT_XML), "w") as o:
            o.writelines(out)


def main():
    xml = SysImgXmlBuilder()

    arg_parser = argparse.ArgumentParser()

    for prop_name in xml.get_cfg_prop_names():
        arg_parser.add_argument("--" + prop_name)

    args = arg_parser.parse_args(sys.argv[1:])

    # Transfer value from configured args to SysImgXmlBuilder
    for prop_name in xml.get_cfg_prop_names():
        arg_value = getattr(args, prop_name)
        if arg_value is not None:
            xml.set_prop_value(prop_name, getattr(args, prop_name))

    not_configured = xml.get_none_cfg_prop_names()

    if len(not_configured):
        print("Error: The following properties are not configured:")
        print(not_configured)
        sys.exit(1)
    else:
        if xml.build():
            print("System Image XML file has been built:\n%s" %
                  xml.get_prop_value(xml.PROP_OUTPUT_XML))
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
