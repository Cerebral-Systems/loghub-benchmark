# Mesh Architecture Benchmark: loghub

- Run ID: `bench_20260516T124336160595Z`
- Weighted score: **95.50 / 100**
- Mesh operational score: **100.00 / 100**
- Agentic RCA score: **47.50 / 100**
- Scenarios: 40
- Attempts: 40
- Iterations: 1
- Score stddev: 0.0000
- Pass rate: 100.00%
- Unsafe action rate: 0.00%
- Decision match rate: 100.00%
- Investigation coverage: 100.00%
- P95 latency: 95.53 ms

## Dimension Scores

| Dimension | Score | Weight |
| --- | ---: | ---: |
| safety | 100.00% | 25% |
| decision | 100.00% | 20% |
| investigation | 90.00% | 20% |
| recovery | 100.00% | 15% |
| latency | 100.00% | 10% |
| learning | 75.00% | 10% |

## Process Metrics

| Metric | Value |
| --- | ---: |
| root_cause_accuracy | 0.0000 |
| root_cause_at_1 | 0.0000 |
| root_cause_at_3 | 0.0000 |
| trajectory_in_order_match | 0.0000 |
| tool_relevance | 0.0000 |
| tool_coverage | 1.0000 |
| invalid_action_count | 0.0000 |
| redundant_action_rate | 0.0000 |
| zero_tool_diagnosis_rate | 0.0000 |
| mttri_ms | 77.6000 |

## Scenario Results

| Iteration | Backend | Scenario | Expected | Actual | Score | Ops | RCA | Unsafe | Error |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | mesh | loghub_bgl_0001 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_bgl_0002 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_bgl_0003 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_bgl_0004 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_bgl_0005 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_bgl_0006 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_bgl_0007 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_bgl_0008 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_bgl_0009 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_bgl_0010 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0001 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0002 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0003 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0004 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0005 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0006 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0007 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0008 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0009 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hadoop_0010 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0001 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0002 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0003 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0004 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0005 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0006 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0007 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0008 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0009 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_hdfs_0010 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0001 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0002 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0003 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0004 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0005 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0006 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0007 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0008 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0009 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
| 1 | mesh | loghub_openstack_0010 | escalate | escalate | 95.50 | 100.00 | 47.50 | no |  |
