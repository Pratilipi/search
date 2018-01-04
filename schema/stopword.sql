USE cms ;

CREATE TABLE stop_word (id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        word VARCHAR(255) CHARACTER SET UTF8 NOT NULL,
                        date_created DATETIME DEFAULT CURRENT_TIMESTAMP(),
                        is_active BOOLEAN DEFAULT 1) ;

CREATE INDEX word_idx ON search_stop_word (word) USING BTREE;
