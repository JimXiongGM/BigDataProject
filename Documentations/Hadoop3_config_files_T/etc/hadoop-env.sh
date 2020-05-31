export HADOOP_OS_TYPE=${HADOOP_OS_TYPE:-$(uname -s)}

case ${HADOOP_OS_TYPE} in
  Darwin*)
    export HADOOP_OPTS="${HADOOP_OPTS} -Djava.security.krb5.realm= "
    export HADOOP_OPTS="${HADOOP_OPTS} -Djava.security.krb5.kdc= "
    export HADOOP_OPTS="${HADOOP_OPTS} -Djava.security.krb5.conf= "
  ;;
esac

export JAVA_HOME=/opt/jdk1.8.0_201
export HADOOP_ROOT_LOGGER="DEBUG,DRFA"