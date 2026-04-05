# Tier 0 

About : Redeemer is a very easy Linux machine which explores the enumeration and exploitation of a Redis database server while showcasing the redis-cli command line utility and basic commands to interact with the Redis service.

note : ```
Redis is an open-source, in-memory data structure store that can be used as a database, cache, message broker, and streaming engine. It belongs to the class of NoSQL databases known as key/value stores, where unique keys map to values of various data types. Redis is widely adopted for its sub-millisecond response times, rich data structures, and versatility across use cases from caching to real-time analytics.```


Date : 16 march 2026

# What I did

```bash
Nmap scan report for 10.129.23.59
Host is up (0.31s latency).
Not shown: 59947 closed tcp ports (conn-refused), 5587 filtered tcp ports (no-response)
PORT     STATE SERVICE
6379/tcp open  redis

Nmap done: 1 IP address (1 host up) scanned in 71.68 seconds
```

Redis is opened on port 6379

```bash
# syntax 1 : connect using host & port, followed by password
$ redis-cli -h host -p port
```


```bash
> redis-cli -h 10.129.23.59 -p 6379
10.129.23.59:6379> help
redis-cli 7.0.15
To get help about Redis commands type:
      "help @<group>" to get a list of commands in <group>
      "help <command>" for help on <command>
      "help <tab>" to get a list of possible help topics
      "quit" to exit

To set redis-cli preferences:
      ":set hints" enable online hints
      ":set nohints" disable online hints
Set your preferences in ~/.redisclirc


```

> Once connected to a Redis server, which command is used to obtain the information and statistics about the Redis server? `info`




```bash 

10.129.23.59:6379> info
# Server
redis_version:5.0.7
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:66bd629f924ac924
redis_mode:standalone
os:Linux 5.4.0-77-generic x86_64
arch_bits:64
multiplexing_api:epoll
atomicvar_api:atomic-builtin
gcc_version:9.3.0
process_id:753
run_id:a19be35ddfb41fdb96974754255fd24b03aa43d6
tcp_port:6379
uptime_in_seconds:1903
uptime_in_days:0
hz:10
configured_hz:10
lru_clock:12072641
executable:/usr/bin/redis-server
config_file:/etc/redis/redis.conf

# Clients
connected_clients:1
client_recent_max_input_buffer:2
client_recent_max_output_buffer:0
blocked_clients:0

# Memory
used_memory:859624
used_memory_human:839.48K
used_memory_rss:5799936
used_memory_rss_human:5.53M
used_memory_peak:859624
used_memory_peak_human:839.48K
used_memory_peak_perc:100.12%
used_memory_overhead:846142
used_memory_startup:796224
used_memory_dataset:13482
used_memory_dataset_perc:21.26%
allocator_allocated:1540408
allocator_active:1880064
allocator_resident:9101312
total_system_memory:2084024320
total_system_memory_human:1.94G
used_memory_lua:41984
used_memory_lua_human:41.00K
used_memory_scripts:0
used_memory_scripts_human:0B
number_of_cached_scripts:0
maxmemory:0
maxmemory_human:0B
maxmemory_policy:noeviction
allocator_frag_ratio:1.22
allocator_frag_bytes:339656
allocator_rss_ratio:4.84
allocator_rss_bytes:7221248
rss_overhead_ratio:0.64
rss_overhead_bytes:-3301376
mem_fragmentation_ratio:7.09
mem_fragmentation_bytes:4982320
mem_not_counted_for_evict:0
mem_replication_backlog:0
mem_clients_slaves:0
mem_clients_normal:49694
mem_aof_buffer:0
mem_allocator:jemalloc-5.2.1
active_defrag_running:0
lazyfree_pending_objects:0

# Persistence
loading:0
rdb_changes_since_last_save:0
rdb_bgsave_in_progress:0
rdb_last_save_time:1773679319
rdb_last_bgsave_status:ok
rdb_last_bgsave_time_sec:0
rdb_current_bgsave_time_sec:-1
rdb_last_cow_size:417792
aof_enabled:0
aof_rewrite_in_progress:0
aof_rewrite_scheduled:0
aof_last_rewrite_time_sec:-1
aof_current_rewrite_time_sec:-1
aof_last_bgrewrite_status:ok
aof_last_write_status:ok
aof_last_cow_size:0

# Stats
total_connections_received:5
total_commands_processed:6
instantaneous_ops_per_sec:0
total_net_input_bytes:323
total_net_output_bytes:11632
instantaneous_input_kbps:0.00
instantaneous_output_kbps:0.00
rejected_connections:0
sync_full:0
sync_partial_ok:0
sync_partial_err:0
expired_keys:0
expired_stale_perc:0.00
expired_time_cap_reached_count:0
evicted_keys:0
keyspace_hits:0
keyspace_misses:0
pubsub_channels:0
pubsub_patterns:0
latest_fork_usec:447
migrate_cached_sockets:0
slave_expires_tracked_keys:0
active_defrag_hits:0
active_defrag_misses:0
active_defrag_key_hits:0
active_defrag_key_misses:0

# Replication
role:master
connected_slaves:0
master_replid:61cf1920f0462f4f7fb846ac4f56f68eb92d98e2
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0

# CPU
used_cpu_sys:1.545365
used_cpu_user:1.081318
used_cpu_sys_children:0.000000
used_cpu_user_children:0.001670

# Cluster
cluster_enabled:0

# Keyspace
db0:keys=4,expires=0,avg_ttl=0
10.129.23.59:6379> 


```

>What is the version of the Redis server being used on the target machine?

```bash
10.129.23.59:6379> info
# Server
redis_version:5.0.7
```

>Which command is used to select the desired database in Redis? `>select`

>How many keys are present inside the database with index 0?

```bash
10.129.23.59:6379> select 0
OK
```

KEYS insctruction to display specific key, error when using it, intuitively did `KEYS *`  to display all the keys. There are 4 keys in the database index 0

```bash
10.129.23.59:6379> KEYS
(error) ERR wrong number of arguments for 'keys' command
10.129.23.59:6379> KEYS *
1) "numb"
2) "flag"
3) "stor"
4) "temp"

```

```bash
10.129.23.59:6379> get flag
"03e1d2b376c37ab3f5319922053953eb"
```

# What I learned

What is redis, and basic redis command usage using redis-cli.