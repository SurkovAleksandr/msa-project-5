package com.task6.batchprocessing.listener;

import com.task6.batchprocessing.model.Product;
import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.core.BatchStatus;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobExecutionListener;
import org.springframework.batch.core.StepExecution;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.DataClassRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class JobCompletionNotificationListener implements JobExecutionListener {

	@Autowired
	private JdbcTemplate jdbcTemplate;

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

            log.info("Job finished: {}", jobExecution.getJobInstance().getJobName());
			log.info("Total items read: {}, write: {}", readCount, writeCount);

			jdbcTemplate
					.query("SELECT productId, productSku, productName, productAmount, productData FROM products order by productId desc limit " + writeCount,
							new DataClassRowMapper<>(Product.class))
					.forEach(person -> log.info("Transformed <{}> in the database.", person));
		}
	}
}
