#Linux 常用netstat命令 实例讲解
#1.查看所有80端口的连接数
netstat -nat|grep -i "80"|wc -l

#2.对连接的IP按连接数量进行排序
netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n

#3.查看TCP连接状态
netstat -nat |awk '{print $6}'|sort|uniq -c|sort -rn
netstat -n | awk '/^tcp/ {++S[$NF]};END {for(a in S) print a, S[a]}'
netstat -n | awk '/^tcp/ {++state[$NF]}; END {for(key in state) print key,"\t",state[key]}'
netstat -n | awk '/^tcp/ {++arr[$NF]};END {for(k in arr) print k,"\t",arr[k]}'
netstat -n |awk '/^tcp/ {print $NF}'|sort|uniq -c|sort -rn
netstat -ant | awk '{print $NF}' | grep -v '[a-z]' | sort | uniq -c

#4.查看80端口连接数最多的20个IP
netstat -anlp|grep 80|grep tcp|awk '{print $5}'|awk -F: '{print $1}'|sort|uniq -c|sort -nr|head -n20
netstat -ant |awk '/:80/{split($5,ip,":");++A[ip[1]]}END{for(i in A) print A,i}' |sort -rn|head -n20

#5.用tcpdump嗅探80端口的访问看看谁最高
tcpdump -i eth0 -tnn dst port 80 -c 1000 | awk -F"." '{print $1"."$2"."$3"."$4}' | sort | uniq -c | sort -nr |head -20

#6.查找较多time_wait连接
netstat -n|grep TIME_WAIT|awk '{print $5}'|sort|uniq -c|sort -rn|head -n20

#7.找查较多的SYN连接
netstat -an | grep SYN | awk '{print $5}' | awk -F: '{print $1}' | sort | uniq -c | sort -nr | more

#8.蜘蛛分析，查看是哪些蜘蛛在抓取内容
/usr/sbin/tcpdump -i eth0 -l -s 0 -w - dst port 80 | strings | grep -i user-agent | grep -i -E 'bot|crawler|slurp|spider'

#9.统计http status
cat access.log |awk '{counts[$(9)]+=1}; END {for(code in counts) print code, counts[code]}'
cat access.log |awk '{print $9}'|sort|uniq -c|sort -rn

#10.日志分析
zcat squid_access.log.tar.gz| awk '{print $10,$7}' |awk 'BEGIN{FS="[ /]"}{trfc[$4]+=$1}END{for(domain in trfc){printf "%st%dn",domain,trfc[domain]}}'

#11.查看数据库
/usr/sbin/tcpdump -i eth0 -s 0 -l -w - dst port 3306 | strings | egrep -i 'SELECT|UPDATE|DELETE|INSERT|SET|COMMIT|ROLLBACK|CREATE|DROP|ALTER|CALL'

#12.统计网站流量（G)
cat /var/log/httpd/access_log |awk '{sum+=$10} END {print sum/1024/1024/1024}'

#13.统计404的连接
awk '($9 ~/404/)' /var/log/httpd/access_log | awk '{print $9,$7}' | sort

#114.列出传输时间超过 30 秒的文件
cat /var/log/httpd/access_log  |awk '($NF > 30){print $7}'|sort -n|uniq -c|sort -nr|head -20

#15.列出最最耗时的页面(超过60秒的)的以及对应页面发生次数
cat /var/log/httpd/access_log |awk '($NF > 60 && $7~/.php/){print $7}'|sort -n|uniq -c|sort -nr|head -100

#16.如果日志最后一列记录的是页面文件传输时间，则有列出到客户端最耗时的页面
cat /var/log/httpd/access_log |awk  '($7~/.php/){print $NF " " $1 " " $4 " " $7}'|sort -nr|head -100

#17.列出输出大于200000byte(约200kb)的exe文件以及对应文件发生次数
cat /var/log/httpd/access_log |awk '($10 > 200000 && $7~/.exe/){print $7}'|sort -n|uniq -c|sort -nr|head -100

#18.访问次数最多的文件或页面,取前20
cat /var/log/httpd/access_log|awk '{print $11}'|sort|uniq -c|sort -nr|head -20

#19.获得访问前10位的ip地址
cat /var/log/httpd/access_log|awk '{print $1}'|sort|uniq -c|sort -nr|head -10
cat /var/log/httpd/access_log|awk '{counts[$(11)]+=1}; END {for(url in counts) print counts[url], url}'

#20.根据端口列进程
netstat -ntlp | grep 80 | awk '{print $7}' | cut -d/ -f1

#查看和本机80端口建立连接并状态在established的所有ip
netstat -an |grep 3306 |grep ESTA |awk '{print$5 "\n"}' |awk 'BEGIN {FS=":"} {print $1 "\n"}' |sort |uniq
 
#输出每个ip的连接数，以及总的各个状态的连接数。
netstat -n | awk '/^tcp/ {n=split($(NF-1),array,":");if(n<=2)++S[array[(1)]];else++S[array[(4)]];++s[$NF];++N} END {for(a in S){printf("%-20s %s\n", a, S[a]);++I}printf("%-20s %s\n","TOTAL_IP",I);for(a in s) printf("%-20s %s\n",a, s[a]);printf("%-20s %s\n","TOTAL_LINK",N);}'
 
#输出和本机3306端口建立连接的每个ip的连接数，以及总的各个状态的连接数。
netstat -n | grep 3306| awk '/^tcp/ {n=split($(NF-1),array,":");if(n<=2)++S[array[(1)]];else++S[array[(4)]];++s[$NF];++N} END {for(a in S){printf("%-20s %s\n", a, S[a]);++I}printf("%-20s %s\n","TOTAL_IP",I);for(a in s) printf("%-20s %s\n",a, s[a]);printf("%-20s %s\n","TOTAL_LINK",N);}'