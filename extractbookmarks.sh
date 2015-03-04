sed -n -e 's/\s*<DT><A HREF="\([^"]*\)".*/\1/p' $1 | sed 's/^[ \t]*//'|sed 's/[ \t]*$//'|sed -n 's#http.*://\([^\/]*\).*#\1#p'|sort|uniq -c|sort -k1
