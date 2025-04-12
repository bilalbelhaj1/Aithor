CREATE TABLE users(
      id INT PRIMARY KEY AUTO_INCREMENT,
      username VARCHAR(20) NOT NULL,
      email VARCHAR(50) NOT NULL,
      `password` VARCHAR(255) NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stories(
      story_id INT primary KEY auto_increment,
      title VARCHAR(255) NOT NULL,
      story TEXT NOT NULL,
      category VARCHAR(50) default 'all',
      generated_at DATETIME default current_timestamp
);

CREATE TABLE stories(
      story_id INT primary KEY auto_increment,
      title VARCHAR(255) NOT NULL,
      story TEXT NOT NULL,
      category VARCHAR(50) default 'all',
      generated_at DATETIME default current_timestamp
);