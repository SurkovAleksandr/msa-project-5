package com.example.batchprocessing;

import org.springframework.batch.core.ItemReadListener;
import org.springframework.stereotype.Component;

@Component
public class StepItemReadListener implements ItemReadListener<Product> {
    @Override
    public void beforeRead() {}

    @Override
    public void afterRead(Product item) {
        System.out.println("Read item: " + item);
    }

    @Override
    public void onReadError(Exception ex) {
        System.err.println("Error reading: " + ex.getMessage());
    }
}
