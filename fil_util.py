# -*- coding: UTF-8 -*- 
import traceback
from dongjsPy.MyLogger import logger
import os

spliter = " kvspliter "#前后都有一个空格符
file_path = "hash.txt"#文件名称


def _get_file(path, mode):
    try:
        f = open(path, mode, encoding='utf-8')
        return f
    except Exception as e:
        trace_message = traceback.format_exc()
        logger.info("获取文件失败，用w自动创建，异常="+trace_message)
        f = open(path, "w", encoding='utf-8')#写的方式打开文件，如果不存在会自动创建,读的方式不会自动创建
        f.close()
        f = open(path, mode, encoding='utf-8')
        return f


# 从文件里面找到key对应的value并返回value
def get_value_by_key(key):
    cur_pid = os.getpid()
    logger.info("cur_pid=[" + str(cur_pid) + "]")
    read_file = _get_file(file_path, "r")
    lines = read_file.readlines()
    read_file.close()
    return _get_value_by_key_lines(lines,key)


def _get_value_by_key_lines(lines,key):
    for line in lines:
        sr_array = line.split(spliter)
        tmp_key = str(sr_array[0])
        value = sr_array[1]
        if key.__eq__(tmp_key):
            return value


# 写的时候如果目标key已经在文件存在就把原来的删除，这个消耗比较大，由于本身的文件内容不多，所以这样做影响不大
def write_key_value_to_file(key, value):
    value = value.replace("\n", "")#key不会有换行符,把value里面的替换掉
    cur_pid = os.getpid()
    logger.info("cur_pid=["+str(cur_pid)+"]")
    read_file = _get_file(file_path, "r")
    line_list = read_file.readlines()
    read_file.close()
    line_store = []
    for line in line_list:
        sr_array = line.split(spliter)
        tmp_key = str(sr_array[0])
        # tmp_value = sr_array[1]
        if key.__eq__(tmp_key):
            continue
            # line_list.remove(line)#文件里面有当前的key，直接删除原来的内容
            #break
        else:
            line_store.append(line.replace("\n",""))

    new_line = key + spliter+value
    line_store.append(new_line)
    write_w_file = _get_file(file_path, "w")
    write_w_file.write("")#清空内容
    write_w_file.close()
    write_file = _get_file(file_path, "a")
    for write_line in line_store:
        write_file.write(write_line)
        write_file.write("\n")
    write_file.close()


if __name__ == '__main__':#test main如果直接运行这个类，那么name的值就是main
    #写数据
    write_key_value_to_file("abc","sql = use rider_center resul\n\ntStatus = Execute Successfully errormessage = None sql =archerTER TABLE rider_xorder_celling_adjustment	DROP INDEX idx_rxccl_source_id,	DROP IarcherX idx_rxccl_riderId_activeFlag,	ADD INDEX idx_riderid_activeflag_endtm (rider_id, active_flag, end_tm),	ADD INDEX idx_activeflag_endtm (active_flag, end_tm) resultStatus = Execute Successfully errormessage = None")
    #读数据
    value = get_value_by_key("abc")
    print(value)
