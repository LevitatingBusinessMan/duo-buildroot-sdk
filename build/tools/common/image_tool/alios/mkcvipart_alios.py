#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import logging
import os
import re


class partition:
    name = ""
    addr = ""
    size = ""
    filename = ""

    def __init__(self, name, addr, size):
        self.name = name
        self.addr = addr
        self.size = size


def parse_args():
    parser = argparse.ArgumentParser(description="Create cvipart.h")
    parser.add_argument("part_table", help="path to partition xml")
    parser.add_argument("output", help="output folder")

    args = parser.parse_args()

    return args


def gen_cvipart_h(output, part_list):
    logging.info("generating cvipart.h")
    with open(os.path.join(output, "cvipart.h"), "w") as of:
        of.write("/* this file should be generated by mkcvipart.py,")
        of.write("please do not modify this file manually*/\n\n")
        of.write("#ifndef CVIPART_H\n")
        of.write("#define CVIPART_H\n")
        env_exist = True

        # If no ENV or U-BOOT ENV has been set in partition.xml, we assume
        # there is no env support
        of.write("#ifndef CONFIG_ENV_IS_NOWHERE\n#define CONFIG_ENV_IS_NOWHERE\n#endif\n")
        of.write("#define CONFIG_ENV_SIZE 0x20000\n")
        env_exist = False

        if env_exist:
            of.write("#define CONFIG_ENV_IS_IN_SPI_FLASH\n")
            of.write("#define CONFIG_ENV_SECT_SIZE  0x10000\n")
        # Generintg MTDPART
        of.write("#define PART_LAYOUT    ")
        of.write('"mtdparts=10000000.cvi-spif:"\n')
        of.write('#define ROOTFS_DEV ""\n')

        # Generintg PART_ENV
        of.write("#define PARTS_OFFSET \\\n")
        for i, p in enumerate(part_list):
            of.write('"%s_PART_OFFSET=%s\\0" \\\n' % (p.name, p.addr))
            if i == len(part_list) - 1:
                of.write(
                    '"%s_PART_SIZE=%s\\0"\n'
                    % (p.name, p.size)
                )
            else:
                of.write(
                    '"%s_PART_SIZE=%s\\0" \\\n'
                    % (p.name, p.size)
                )

        of.write("#endif")
        logging.info("Done!")


def get_part(str_list):
    name = addr = size = ""
    str = ''.join(str_list).replace(" ", "")
    kv_list = str.split(",")
    for i in kv_list:
        key = i.split(":")[0]
        val = i.split(":")[1]
        if(key == "name"):
            name = val
        elif(key == "address"):
            addr = val
        elif(key == "size"):
            size = val

    part = partition(name, addr, size)

    return part


def parse_part_table(file):
    part_list = []
    fp = open(file, "r")
    sample = fp.readlines()
    p = re.compile(r'[{](.*?)[}]', re.S)
    for i in sample:
        if "-" in i:
            str_list = re.findall(p, i)
            partition = get_part(str_list)
            part_list.append(partition)
    fp.close()

    return part_list


def main():
    args = parse_args()
    part_list = parse_part_table(args.part_table)

    gen_cvipart_h(args.output, part_list)


if __name__ == "__main__":
    main()