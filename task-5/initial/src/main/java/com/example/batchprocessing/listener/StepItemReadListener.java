package com.example.batchprocessing.listener;

import com.example.batchprocessing.model.Product;
import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.core.ItemReadListener;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class StepItemReadListener implements ItemReadListener<Product> {

    @Override
    public void beforeRead() {}

    @Override
    public void afterRead(Product item) {
        log.info("Read item: " + item);
    }

    @Override
    public void onReadError(Exception ex) {
        log.info("Error reading: " + ex.getMessage());
    }
}
