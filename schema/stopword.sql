USE cms ;

CREATE TABLE search_stop_word (id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                               language ENUM('HINDI', 'MARATHI', 'TAMIL', 'TELUGU', 'BENGALI', 'KANNADA', 'GUJARATI', 'MALAYALAM') NOT NULL,
                               word VARCHAR(255) CHARACTER SET UTF8 NOT NULL,
                               date_created DATETIME DEFAULT CURRENT_TIMESTAMP(),
                               is_active BOOLEAN DEFAULT 1) ;

CREATE INDEX language_idx ON search_stop_word (language) USING BTREE;

