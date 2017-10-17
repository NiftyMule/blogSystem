DROP TABLE post;

CREATE TABLE IF NOT EXISTS post (
  	post_id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(50) NOT NULL,
	content TEXT NOT NULL,
	ip_address VARCHAR(20) NOT NULL,
	submission_time DATE,
  	PRIMARY KEY ( post_id )
) character set = utf8;