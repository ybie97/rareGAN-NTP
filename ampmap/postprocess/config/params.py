[all]
kl_thresh=0.08
af_thresh=10
data_path=./data_dir/
sv_path=./signatures/




[ntp_cnt]
ipp  =field_inputs_ntpControl
proto_name=query_searchout_NTPControl_AND_20200608

[ntp_pvt]
ipp  =field_inputs_ntpPrivate
proto_name=query_searchout_NTPPrivate_

[ntp_normal]
ipp  =field_inputs_ntpNormal
proto_name=query_searchout_NTPNormal_AND_20200608

[group1]
l1=[ntp_cnt_or,ntp_pvt_or,ntp_normal_or]

[group2]
l1=[ntp_cnt,ntp_pvt,ntp_normal]

[group3]
l1=[snmp_next_or,snmp_bulk_or,snmp_get_or]

[group4]
l1=[snmp_next,snmp_bulk,snmp_get]