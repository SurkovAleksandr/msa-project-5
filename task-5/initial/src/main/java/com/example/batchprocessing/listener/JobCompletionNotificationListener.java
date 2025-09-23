package com.example.batchprocessing.listener;

import com.example.batchprocessing.model.Product;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.Metrics;
import io.prometheus.metrics.core.metrics.Gauge;
import io.prometheus.metrics.exporter.pushgateway.PushGateway;
import io.prometheus.metrics.model.snapshots.Unit;
import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.core.BatchStatus;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobExecutionListener;
import org.springframework.batch.core.StepExecution;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.DataClassRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Slf4j
@Component
public class JobCompletionNotificationListener implements JobExecutionListener {

	@Autowired
	private JdbcTemplate jdbcTemplate;

	PushGateway pgw = PushGateway.builder()
			.address("pushgateway:9091")
			.job("pushgateway")
			.build();

	private Gauge metricReadCount = Gauge.builder()
			.name("readCount")
			.help("Count of reding rows")
			.register();
	private Gauge metricWriteCount = Gauge.builder()
			.name("writeCount")
			.help("Count of writing rows")
			.register();

	@Override
	public void afterJob(JobExecution jobExecution) {
		if (jobExecution.getStatus() == BatchStatus.COMPLETED) {
			log.info("!!! JOB FINISHED! Time to verify the results");

			long readCount = jobExecution.getStepExecutions().stream()
					.mapToLong(StepExecution::getReadCount)
					.sum();

			long writeCount = jobExecution.getStepExecutions().stream()
					.mapToLong(StepExecution::getWriteCount)
					.sum();

			metricReadCount.set(readCount);
			metricWriteCount.set(writeCount);

			try {
				pgw.push();
			} catch (IOException ex) {
				log.error("Ошибка отправки метрик в Pushgateway", ex);
			}

            log.info("Job finished: {}", jobExecution.getJobInstance().getJobName());
			log.info("Total items read: {}", readCount);

			jdbcTemplate
					.query("SELECT productId, productSku, productName, productAmount, productData FROM products", new DataClassRowMapper<>(Product.class))
					.forEach(person -> log.info("Transformed <{}> in the database.", person));
		}
	}
}
