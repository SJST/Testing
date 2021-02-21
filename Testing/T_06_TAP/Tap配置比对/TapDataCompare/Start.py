# -*- coding: utf-8 -*-

# @Project  : TapDataCompare
# @File     : Start.py
# @Date     : 2021-01-27
# @Author   : Administrator
# @Info     :
# @Introduce:
import os, psycopg2, copy
import pandas as pd
from pandas import DataFrame


class Constant(object):
    DirName = 'T03_Config'
    FileName = 'Config.txt'
    DataDir = 'T02_Data'
    ClassErrorMessage = '调用属性异常'
    FatherDirFlag = ".."
    DirSpiltFlag = "\\"
    IP = 'ip'
    Port = 'port'
    User = 'userid'
    Password = 'password'
    DataBase = 'database'
    JsonError = 'JsonError'
    Zero = 0
    One = 1
    ExceptErrorList = {
        'JsonError': '初始化配置失败，请检查配置格式是否正确'
    }
    Target = 'target'
    Source = 'source'
    CommonSql = "select * from "
    Schema = 'db_conf'
    Point = '.'
    TableName = ['t_pz_pzxx', 't_pz_system', 't_pz_zxtdy', 't_pz_pzdm', 't_pz_pzfz']
    ConfigInfo = 't_pz_pzxx'
    SystemInfo = 't_pz_system'
    AppInfo = 't_pz_zxtdy'
    GroupInfo = 't_pz_pzfz'
    SingleInfo = 't_pz_pzdm'
    SystemBh = 'c_bh_system'
    AppBh = 'c_xtbh'
    GroupBh = 'c_fzbh'
    SingleBh = 'c_pzdm'
    MC = 'c_mc'
    BH = 'c_bh'
    CodeTypeKey = 'c_pzdm'
    ZT = {"1": "未找到配置项", "2": "配置项存在问题", "3": "配置项匹配"}
    Map = {
        "c_bh_system": "系统编号",
        'c_bh': '主键',
        'c_xtbh': '应用编号',
        'pzbm': '配置编码',
        'n_wh': '是否可维护',
        'c_mrz': '默认值',
        'n_yx': '是否有效'
    }


ConstantClass = Constant()


def list_to_dict(list_data) -> dict:
    data = copy.deepcopy(list_data)
    dict_data = {}
    for i in data:
        dict_data.update(i)

    if 'c_fzbh' in dict_data.keys() and dict_data['c_fzbh'] == 't3c00000000000000000000000splxwh':
        dict_data = None
    return dict_data


def filter_dict(data1, value1, key2, *args) -> dict:
    """
    @Info:根据key2 和value1 定位要获取的data1中的map 在根据arg中的key值 得到需要使用的字段数据
    :param data1: 目标数据 [{}]
    :param value1: 连接两个数据的value值
    :param key2: 源数据中连接value值 对应的 key值
    :param args: 需要在 data1 中取到是数据的key值
    :return: 返回map 目标数据中的 key value 值
    """
    result = {}
    for i in data1:
        if i[key2] == value1:
            for j in args:
                if j in i.keys():
                    result[j] = i[j]
        if result:
            break
    return result


def update_dict(dict2, *args):
    """
        根据 arg中传入的 字段 将 dict中该字段的添加到 dict1 中 arg 是dict格式 key为dict2 中key value 为添加到dict1中所
        使用key 返回值为 dict1
    :param dict2: 源 dict
    :param args: 字段
    :return: 目标dict
    """
    dict1 = {}
    field_list = args[0]
    for key in dict2:
        if args and key in field_list.keys():
            dict1[field_list[key]] = dict2[key]
    return dict1


def get_dir_file(path):
    pwd = os.getcwd()
    grader_father = os.path.abspath(os.path.dirname(pwd) + ConstantClass.FatherDirFlag)
    target_dir = grader_father + ConstantClass.DirSpiltFlag + \
                 path
    


class Application(object):

    def __init__(self, name):
        """
        初始化 数据
        :return: 开始执行的功能
        """
        self.name = name
        print(name)

    def main(self):
        # 调用常量类
        Main = OperaClassApplication()
        Main.main()


class OperaClassApplication(object):

    def __init__(self):
        pass

    def main(self):
        # 根据配置文件获取 数据库信息
        ExportClass = ExportData(ConstantClass.DirName, ConstantClass.FileName)
        db_info = ExportClass.export_main()
        #  获取数据库数据
        GetDataClass = GetData(db_info)
        db_data = GetDataClass.get_data_main()
        # 处理数据为带比较数据
        ChangeDataClass = ChangeData(db_data)
        wait_compare_data = ChangeDataClass.deal_data_main()
        # 比较数据
        CompareDataClass = CompareData(wait_compare_data)
        wait_write_data = CompareDataClass.current_compare_data()
        WriteDataClass = WriteData(wait_write_data)
        WriteDataClass.write_main()


class GetData(object):
    dict_data = {}
    finally_data = {}
    init_data = None

    def __init__(self, data_info):
        self.data_info = data_info

    def get_data_main(self):
        self.get_data_file()
        self.get_data()
        return self.dict_data

    def get_data_file(self):
        """
            @ Info 兼容上线第一次比对 如果存在准备好的文件 则取准备好的文件
        """

    def get_data(self):
        common_sql = ConstantClass.CommonSql + ConstantClass.Schema + ConstantClass.Point
        if self.init_data:
            # 如果 init data 有值 则认为 是家里与现场比较 不在获取 source数据库的的信息
            del self.data_info['source']
        for one_key in self.data_info:
            ConnectClass = ConnectDB(self.data_info[one_key])
            key_data_dict = {}
            for one_table in ConstantClass.TableName:
                ConnectClass.sql = common_sql + one_table
                table_data = ConnectClass.connect_main()
                key_data_dict[one_table] = table_data
            self.dict_data[one_key] = key_data_dict


class ChangeData(object):
    config_info = None
    finally_data = {}

    def __init__(self, wait_deal_data):
        self.wait_deal_data = wait_deal_data

    def deal_data_main(self):
        self.deal_data()
        return self.finally_data

    def deal_data(self):
        data = copy.deepcopy(self.wait_deal_data)

        for one in data:
            OnceData = data[one]
            self.config_info = OnceData[ConstantClass.ConfigInfo]
            system_info = OnceData[ConstantClass.SystemInfo]
            app_info = OnceData[ConstantClass.AppInfo]
            group_info = OnceData[ConstantClass.GroupInfo]
            single_info = OnceData[ConstantClass.SingleInfo]
            self.change_system_info(system_info, 'SystemMC', ConstantClass.SystemBh)
            self.change_system_info(app_info, 'AppMC', ConstantClass.AppBh)
            self.change_system_info(group_info, 'GroupMC', ConstantClass.GroupBh)
            self.change_single_info(single_info, 'SingleData')
            self.finally_data[one] = self.config_info

    def change_system_info(self, system_info, key, source_key):
        for one_config_data in self.config_info:
            Bh = ConstantClass.BH
            system_bh = one_config_data[source_key]
            filter_result = filter_dict(system_info, system_bh, Bh, ConstantClass.MC)
            conditions = {ConstantClass.MC: key}
            deal_result = update_dict(filter_result, conditions)
            one_config_data.update(deal_result)

    def change_single_info(self, single_info, key):
        for one_config_data in self.config_info:
            code_type_key = ConstantClass.CodeTypeKey
            source_value = one_config_data[code_type_key]
            one_config_data[key] = self.get_single_value(single_info, code_type_key, source_value)

    @staticmethod
    def get_single_value(single_data, key, value) -> dict:
        result = {}
        for i in single_data:
            if i[key] == value:
                result[i['c_dm']] = i['c_dmsm']
        return result


class CompareData(object):
    result_data = {}
    result_list = []

    def __init__(self, wait_compare_data):
        self.source_data = wait_compare_data['sourceDB']
        self.target_data = wait_compare_data['targetDB']

    def current_compare_data(self):

        for one_data in self.source_data:
            pzx_key = one_data['c_key']
            group_key = one_data['c_fzbh']
            self.get_common_data(one_data)
            # 与文家沟通 确定一对一配置 需要使用 分组编号和 配置项 做匹配
            target_data_list = [i for i in self.target_data if i['c_key'] == pzx_key and i['c_fzbh'] == group_key]
            if target_data_list:
                target_one_data = target_data_list[ConstantClass.Zero]
                # 比对系统
                self.compare_data(one_data, 'c_bh_system', target_one_data)
                # 比对应用
                self.compare_data(one_data, 'c_xtbh', target_one_data)
                # 比对主键
                self.compare_data(one_data, 'c_bh', target_one_data)
                # 比对是否可维护
                self.compare_data(one_data, 'n_wh', target_one_data)
                # 比对有效
                self.compare_data(one_data, 'n_yx', target_one_data)
                # 比对默认值
                self.compare_data(one_data, 'c_mrz', target_one_data)
            else:
                # 如果找不到配置项 直接以预设好的进行输出
                self.result_list.append(self.result_data)

        return self.result_list

    def compare_data(self, one_data, key, target_data):
        result = copy.deepcopy(self.result_data)
        source = one_data[key]
        target = target_data[key]
        if target == source:
            result['比对结果'] = '配置项匹配'
        else:
            result['比对结果'] = '配置项存在差异'
        result['比对项'] = ConstantClass.Map[key]
        result['源库'] = source
        result['目标库'] = target
        self.result_list.append(result)

    def get_common_data(self, one_data):
        self.result_data = {}
        SystemMC = one_data['SystemMC']
        GroupMC = one_data['GroupMC']
        KeyMC = one_data['c_mc']
        KeyValue = one_data['c_key']
        self.result_data['比对结果'] = '未找到配置项'
        self.result_data['系统名称'] = SystemMC
        self.result_data['分组名称'] = GroupMC
        self.result_data['配置名称'] = KeyMC
        self.result_data['配置项key'] = KeyValue
        self.result_data['比对项'] = ''
        self.result_data['源库'] = ''
        self.result_data['目标库'] = ''


class WriteData(object):
    result = []
    title = None

    def __init__(self, data):
        self.data = data

    def write_main(self):
        self.deal_write_data()
        self.write_result()

    def deal_write_data(self):

        self.title = list(self.data[0].keys())
        for i in self.data:
            j = list(i.values())
            self.result.append(j)

    def write_result(self):
        # 创建一个空的excel文件
        nan_excel = pd.DataFrame(self.result, columns=self.title)
        pwd = os.getcwd()
        grader_father = os.path.abspath(os.path.dirname(pwd) + ConstantClass.FatherDirFlag)
        path = grader_father + ConstantClass.DirSpiltFlag + "T04_Result" + ConstantClass.DirSpiltFlag
        filename = 'result.xlsx'
        sheets = ['Result']

        # 打开excel
        writer = pd.ExcelWriter(path + filename)
        # sheets是要写入的excel工作簿名称列表
        for sheet in sheets:
            nan_excel.set_index('系统名称', inplace=True)
            nan_excel.to_excel(writer, sheet_name=sheet)

        # 保存writer中的数据至excel
        # 如果省略该语句，则数据不会写入到上边创建的excel文件中
        writer.save()


class ExportData(object):
    ExportOutDataAddress = None
    dict_config_content = None

    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    def __getattr__(self, item):
        return ConstantClass.ClassErrorMessage

    def export_main(self):
        self.spilt_config_path()
        self.get_config_content()
        return self.dict_config_content

    def spilt_config_path(self):
        """
          Description: 根据当前项目目录 拼接外部 文件地址

        """
        pwd = os.getcwd()
        grader_father = os.path.abspath(os.path.dirname(pwd) + ConstantClass.FatherDirFlag)
        self.ExportOutDataAddress = grader_father + ConstantClass.DirSpiltFlag + \
                                    self.path + ConstantClass.DirSpiltFlag + self.filename

    def get_config_content(self):
        """
         获取配置内容
        :return:
        """
        try:
            file = open(self.ExportOutDataAddress, 'r', encoding="UTF-8")
            file_content = file.read()
            # eval  将字典字符串转字典。
            self.dict_config_content = eval(file_content)
        except Exception as e:
            print(ConstantClass.ExceptErrorList[ConstantClass.JsonError])


class ConnectDB(object):
    cur = None
    sql_result = []
    filter_rule = None
    sql = None
    conn = None
    rows = None
    desc = None

    FieldResultData = []

    def __init__(self, db_info):
        self.Database = db_info[ConstantClass.DataBase]
        self.User = db_info[ConstantClass.User]
        self.Password = db_info[ConstantClass.Password]
        self.host = db_info[ConstantClass.IP]
        self.port = db_info[ConstantClass.Port]

    def __getattr__(self, item):
        return ConstantClass.ClassErrorMessage

    def connect_main(self):
        self.connect_target_db()
        self.execute_sql()
        self.get_target_db_xx()
        return self.sql_result

    def connect_target_db(self):
        self.conn = psycopg2.connect(database=self.Database, user=self.User, password=self.Password, host=self.host,
                                     port=self.port)
        self.cur = self.conn.cursor()

    def execute_sql(self):
        self.cur.execute(self.sql)
        self.rows = self.cur.fetchall()
        self.desc = self.cur.description
        self.cur.close()
        self.conn.close()

    def get_target_db_xx(self):
        self.sql_result = []
        rows = copy.deepcopy(self.rows)
        desc = copy.deepcopy(self.desc)
        for j in rows:
            data_list = [{desc[i][ConstantClass.Zero]: j[i]} for i in range(len(rows[ConstantClass.Zero]))]
            dict_list = list_to_dict(data_list)
            if dict_list:
                self.sql_result.append(dict_list)


if __name__ == '__main__':
    a = Application('Tap数据比对即将开始..')
    a.main()
