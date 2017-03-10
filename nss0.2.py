# -*- coding:utf-8 -*-
import urllib
import urllib2
import json
import sys

def getPDFFromNet(html_page, total_page):
    origin = 'http://www.cninfo.com.cn/'
    localDir = 'D:\downloadPDF\\'# 下载PDF文件需要存储在本地的文件夹

    unifile = json.loads(html_page)
    print 'totalAnnouncement:', unifile['totalAnnouncement']

    for f in range(0, total_page):
        if unifile['announcements'][f]['adjunctType'] == 'PDF':
            localPDF = localDir +unifile['announcements'][f]['announcementId']\
                   +unifile['announcements'][f]['announcementTitle'] +".pdf"
        elif unifile['announcements'][f]['adjunctType'] is None:
            localPDF = localDir +unifile['announcements'][f]['announcementId']\
                   +unifile['announcements'][f]['announcementTitle'] +".html"
        else:
            print "File type needs support:", unifile['announcements'][f]['adjunctType'], ", call tim."
            localPDF = localDir +unifile['announcements'][f]['announcementId']\
                   +unifile['announcements'][f]['announcementTitle'] +"."+unifile['announcements'][f]['adjunctType']
        try:
            print 'download file:', localPDF
            urllib.urlretrieve(origin+unifile['announcements'][f]['adjunctUrl'], localPDF)  # 按照url进行下载，并以其文件名存储到本地目录
        except Exception, e:
            print e
            continue
        # print 'finish download 1'
        # time.sleep(5)


if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
    page_size = 30
    page_num = 1

    send_headers = {
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

    values = {'stock': '',  # 分号里直接填写股票代码 代码和关键字不能同时填
              'searchkey': '公司;',  # 填写搜索关键字，示例为 青岛国货集团股份有限公司2001年第一次
              'plate': 'szmb;',  # 填写板块代码，具体代码见上面，示例为 szmb/深圳主板
              'category': 'category_gddh_szsh;',  # 填写公告类别代码，示例为 category_gddh_szsh/股东大会
              'trade': '金融业;',  # 填写行业，示例为 金融业
              'column': 'szse',
              'columnTitle': '历史公告查询',
              'pageNum': page_num,
              'pageSize': page_size,
              'tabName': 'fulltext',
              'sortName': '',
              'sortType': '',
              'limit': '',
              'showTitle': '',
              'seDate': '2000-01-01 ~ 2017-01-02'  # 按格式填写时间，示例为 2000年1月1日到2017年1月2日
              }
    #
    # print '需要输入相关参数来开始任务,如果不填则直接按回车：\n '
    # flag = True
    # while flag:
    #     print 'stock, 直接填写股票代码 代码和关键字不能同时填\n'
    #     values['stock'] = raw_input('>>')
    #     print 'searchkey, 填写搜索关键字\n'
    #     values['searchkey'] = raw_input('>>')
    #     print 'plate, 填写板块代码，多个板块以分号";"分隔\n'
    #     print 'sz/深市公司 szmb/深圳主板 szzx/中小板 szcy/创业板 shmb/沪市主板\n'
    #     values['plate'] = raw_input('>>')
    #     print 'category,填写公告类别代码\n'
    #     print '#           category_ndbg_szsh/年度报告;category_bndbg_szsh/半年度报告;category_yjdbg_szsh/一季度报告;'
    #     print '#           category_sjdbg_szsh/三季度报告;category_scgkfx_szsh/首次公开发行及上市;category_pg_szsh/配股;'
    #     print '#           category_zf_szsh/增发;category_kzhz_szsh/可转换债券;category_qzxg_szsh/权证相关公告;'
    #     print '#           category_qtrz_szsh/其他融资;category_qyfpxzcs_szsh/权益及限制出售股份;'
    #     print '#           category_gqbd_szsh/股权变动;category_jy_szsh/交易;category_gddh_szsh/股东大会;'
    #     print '#           category_cqfxyj_szsh/澄清风险业绩预告;category_tbclts_szsh/特别处理和退市;'
    #     print '#           category_bcgz_szsh/补充及更正;category_zjjg_szsh/中介机构报告;category_ssgszd_szsh/上市公司制度;'
    #     print '#           category_zqgg_szsh/债券公告;category_qtzdsx_szsh/其它重大事项;category_tzzgx_szsh/投资者关系信息;'
    #     print '#           category_dshgg_szsh/董事会公告;category_jshgg_szsh/监事会公告'
    #     values['category'] = raw_input('>>')
    #     print 'trade,填写行业\n'
    #     print '#           农、林、牧、渔业;采矿业;制造业;电力、热力、燃气及水生产和供应业;建筑业;批发和零售业;交通运输、仓储和邮政业;'
    #     print '#           住宿和餐饮业;信息传输、软件和信息技术服务业;金融业;房地产业;租赁和商务服务业;科学研究和技术服务业;'
    #     print '#           水利、环境和公共设施管理业;居民服务、修理和其他服务业;教育;卫生和社会工作;文化、体育和娱乐业;综合;'
    #     values['trade'] = raw_input('>>')
    #     print 'seDate,按格式填写时间\n'
    #     print '2000-01-01 ~ 2017-01-02 按格式填写时间，示例为 2000年1月1日到2017年1月2日'
    #     values['seDate'] = raw_input('>>')
    #     flag = False
    #
    # proxy_support = urllib2.ProxyHandler({"http": "http://web-proxyhk.oa.com:8080"})
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, send_headers)
    response = urllib2.urlopen(req)
    the_page = response.read()

    unifile = json.loads(the_page)
    getPDFFromNet(the_page, unifile['totalAnnouncement'])
    page_num += 1
    print 'page_num:', page_num
    values['pageNum'] += 1
    print values['pageNum']

    # 第一次获取页面后拿到对应的总公告数，判断还剩余多少页
    left_pages = unifile['totalAnnouncement'] % page_size
    print 'left_pages:', left_pages
    if left_pages is 0:
        total_pages = unifile['totalAnnouncement'] / page_size
    else:
        total_pages = unifile['totalAnnouncement'] / page_size + 1

    print 'total_pages:', total_pages
    if total_pages > 1:
        for s in range(2, total_pages + 1):
            print values['pageNum']
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data, send_headers)
            response = urllib2.urlopen(req)
            the_page = response.read()

            unifile = json.loads(the_page)
            print unifile['announcements'][0]['announcementTitle']
            if (total_pages + 1 - s) == 1:
                getPDFFromNet(the_page, unifile['totalAnnouncement'] - (s - 1) * page_size)
            else:
                getPDFFromNet(the_page, page_size)
            page_num += 1

