# -*- coding:utf-8 -*-
import urllib
import urllib2
import json
import sys


def download_file_from_net(json_page, total_announce_num):
    origin_host = 'http://www.cninfo.com.cn/'
    local_dir = 'D:\downloadPDF\\'  # 下载PDF文件需要存储在本地的文件夹

    print 'Total announcements:', json_page['totalAnnouncement']

    for f in range(0, total_announce_num):
        local_file_dir = local_dir + json_page['announcements'][f]['announcementId'] \
                         + json_page['announcements'][f]['announcementTitle']

        if json_page['announcements'][f]['adjunctType'] == 'PDF':
            local_file_dir += ".pdf"
        elif json_page['announcements'][f]['adjunctType'] is None:
            local_file_dir += ".html"
        else:
            print "File type needs support:", json_page['announcements'][f]['adjunctType'], ", call tim."
            local_file_dir += "." + json_page['announcements'][f]['adjunctType']

        try:
            print 'Download file:', local_file_dir
            # 按照url进行下载，并以其文件名存储到本地目录
            urllib.urlretrieve(origin_host + json_page['announcements'][f]['adjunctUrl'],local_file_dir)
        except Exception, e:
            print e
            continue


def get_json_from_url(input_values, url):
    post_headers = {
        'Host': 'www.cninfo.com.cn',
        'Connection': 'keep-alive',
        # 'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://www.cninfo.com.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Referer': 'http://www.cninfo.com.cn/cninfo-new/announcement/show',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
    }

    post_data = urllib.urlencode(input_values)
    request_js_packet = urllib2.Request(url, post_data, post_headers)
    html_page = urllib2.urlopen(request_js_packet).read()
    json_page = json.loads(html_page)
    return json_page


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    fetch_js_url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
    single_page_announce_num = 30


    # 以下参数均可为空，允许多个参数的用分号分隔
    # stock:直接填写股票代码 代码和关键字不能同时填
    # searchkey：填写关键字
    # plate：sz/深市公司 szmb/深圳主板 szzx/中小板 szcy/创业板 shmb/沪市主板
    # category：category_ndbg_szsh/年度报告;category_bndbg_szsh/半年度报告;category_yjdbg_szsh/一季度报告;
    #           category_sjdbg_szsh/三季度报告;category_scgkfx_szsh/首次公开发行及上市;category_pg_szsh/配股;
    #           category_zf_szsh/增发;category_kzhz_szsh/可转换债券;category_qzxg_szsh/权证相关公告;
    #           category_qtrz_szsh/其他融资;category_qyfpxzcs_szsh/权益及限制出售股份;
    #           category_gqbd_szsh/股权变动;category_jy_szsh/交易;category_gddh_szsh/股东大会;
    #           category_cqfxyj_szsh/澄清风险业绩预告;category_tbclts_szsh/特别处理和退市;
    #           category_bcgz_szsh/补充及更正;category_zjjg_szsh/中介机构报告;category_ssgszd_szsh/上市公司制度;
    #           category_zqgg_szsh/债券公告;category_qtzdsx_szsh/其它重大事项;category_tzzgx_szsh/投资者关系信息;
    #           category_dshgg_szsh/董事会公告;category_jshgg_szsh/监事会公告
    # trade：农、林、牧、渔业;采矿业;制造业;电力、热力、燃气及水生产和供应业;建筑业;批发和零售业;交通运输、仓储和邮政业;住宿和餐饮业;信息传输、
    #        软件和信息技术服务业;金融业;房地产业;租赁和商务服务业;科学研究和技术服务业;水利、环境和公共设施管理业;居民服务、修理和其他服务业;
    #        教育;卫生和社会工作;文化、体育和娱乐业;综合;

    search_values = {'stock': '',  # 分号里直接填写股票代码 代码和关键字不能同时填
                     'searchkey': '公司;',  # 填写搜索关键字，示例为 青岛国货集团股份有限公司2001年第一次
                     'plate': 'szmb;',  # 填写板块代码，具体代码见上面，示例为 szmb/深圳主板
                     'category': 'category_gddh_szsh;',  # 填写公告类别代码，示例为 category_gddh_szsh/股东大会
                     'trade': '金融业;',  # 填写行业，示例为 金融业
                     'column': 'szse',
                     'columnTitle': '历史公告查询',
                     'pageNum': 1,
                     'pageSize': single_page_announce_num,
                     'tabName': 'fulltext',
                     'sortName': '',
                     'sortType': '',
                     'limit': '',
                     'showTitle': '',
                     'seDate': '2000-01-01 ~ 2017-01-02'  # 按格式填写时间，示例为 2000年1月1日到2017年1月2日
                     }
    # 获取首页的基础json结构
    the_json_page = get_json_from_url(search_values, fetch_js_url)
    # 拿到总公告数后，判断总共页数及零散页公告数
    scattered_announce_num = the_json_page['totalAnnouncement'] % single_page_announce_num
    print 'scattered_announce_num:', scattered_announce_num
    if scattered_announce_num is 0:
        total_pages = the_json_page['totalAnnouncement'] / single_page_announce_num
    else:
        total_pages = the_json_page['totalAnnouncement'] / single_page_announce_num + 1
    print 'total_pages:', total_pages
    # 遍历每一页进行下载
    for page_index in range(1, total_pages + 1):
        print "Current page number:", search_values['pageNum']
        the_json_page = get_json_from_url(search_values, fetch_js_url)

        if total_pages == page_index:
            download_file_from_net(the_json_page,
                                   the_json_page['totalAnnouncement'] - (total_pages - 1) * single_page_announce_num)
        else:
            download_file_from_net(the_json_page, single_page_announce_num)
            search_values['pageNum'] += 1
