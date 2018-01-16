USE cms ;

CREATE TABLE stop_word (id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        word VARCHAR(255) CHARACTER SET UTF8 NOT NULL,
                        date_created DATETIME DEFAULT CURRENT_TIMESTAMP(),
                        is_active BOOLEAN DEFAULT 1) ;

CREATE INDEX word_idx ON stop_word (word) USING BTREE;
CREATE INDEX is_active_idx ON stop_word (is_active) USING BTREE;
