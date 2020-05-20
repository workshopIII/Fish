-- phpMyAdmin SQL Dump
-- version 4.8.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 2020-05-20 11:05:27
-- 服务器版本： 10.1.32-MariaDB
-- PHP Version: 7.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ws3`
--

-- --------------------------------------------------------

--
-- 表的结构 `course`
--

CREATE TABLE `course` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `CourseId` varchar(50) NOT NULL,
  `CourseName` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `course`
--

INSERT INTO `course` (`create_time`, `status`, `CourseId`, `CourseName`) VALUES
(NULL, NULL, 'ACHN0763', 'iykgjrnf'),
(NULL, NULL, 'CFIG7894', 'wgvzsxki'),
(0, NULL, 'DLJF0718', 'zlspxykft'),
(NULL, NULL, 'MAQI9125', 'nxblfkc');

-- --------------------------------------------------------

--
-- 表的结构 `courseteamstudent`
--

CREATE TABLE `courseteamstudent` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `rid` int(11) NOT NULL,
  `CourseId` varchar(50) NOT NULL,
  `Tid` int(11) DEFAULT NULL,
  `StudentID` varchar(50) DEFAULT NULL,
  `sectionNo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `course_student`
--

CREATE TABLE `course_student` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `rrrid` int(11) NOT NULL,
  `studentID` varchar(50) DEFAULT NULL,
  `CourseId` varchar(50) NOT NULL,
  `sectionNo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `course_teacher`
--

CREATE TABLE `course_teacher` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `rrid` int(11) NOT NULL,
  `staffID` varchar(50) DEFAULT NULL,
  `CourseId` varchar(50) NOT NULL,
  `sectionNo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `course_teacher`
--

INSERT INTO `course_teacher` (`create_time`, `status`, `rrid`, `staffID`, `CourseId`, `sectionNo`) VALUES
(0, NULL, 1, '90641857', 'DLJF0718', '1001'),
(NULL, NULL, 2, '90641857', 'MAQI9125', '1002'),
(NULL, NULL, 3, '90641857', 'CFIG7894', '1001'),
(NULL, NULL, 4, '90641857', 'ACHN0763', '1003'),
(NULL, NULL, 5, '4586793', 'XQJL9360', '1001'),
(NULL, NULL, 6, '12645307', 'NGCW3947', '1003'),
(NULL, NULL, 7, '36092741', 'CFIG7894', '1002'),
(NULL, NULL, 8, '9483562', 'DLJF0718', '1001'),
(NULL, NULL, 9, '4613928', 'QSFM4231', '1002'),
(NULL, NULL, 10, '85970312', 'CFEI4961', '1001');

-- --------------------------------------------------------

--
-- 表的结构 `dividein`
--

CREATE TABLE `dividein` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `did` int(11) NOT NULL,
  `CourseId` varchar(50) NOT NULL,
  `staffID` varchar(50) NOT NULL,
  `methodNo` int(11) NOT NULL,
  `numberPergroup` int(11) DEFAULT NULL,
  `totalStu` int(11) DEFAULT NULL,
  `rest` int(11) DEFAULT NULL,
  `groupNNormal` int(11) DEFAULT NULL,
  `totalGroup` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `invitation`
--

CREATE TABLE `invitation` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `iid` int(11) NOT NULL,
  `CourseId` varchar(50) NOT NULL,
  `sectionNo` varchar(50) NOT NULL,
  `studentID` varchar(50) DEFAULT NULL,
  `selection` varchar(50) DEFAULT NULL,
  `confirm` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `leader`
--

CREATE TABLE `leader` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `lid` int(11) NOT NULL,
  `StudentID` varchar(50) NOT NULL,
  `CourseId` varchar(50) NOT NULL,
  `sectionNo` varchar(50) NOT NULL,
  `Tid` int(11) DEFAULT NULL,
  `contribution` float DEFAULT NULL,
  `bonus` float DEFAULT NULL,
  `default` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `member`
--

CREATE TABLE `member` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `mid` int(11) NOT NULL,
  `StudentID` varchar(50) DEFAULT NULL,
  `CourseId` varchar(50) NOT NULL,
  `sectionNo` varchar(50) NOT NULL,
  `contribution` float DEFAULT NULL,
  `tid` int(11) DEFAULT NULL,
  `vote` varchar(50) DEFAULT NULL,
  `default` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `randnumber`
--

CREATE TABLE `randnumber` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `listid` int(11) NOT NULL,
  `num` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `student`
--

CREATE TABLE `student` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `StudentID` varchar(50) NOT NULL,
  `StuName` varchar(30) DEFAULT NULL,
  `GPA` varchar(30) DEFAULT NULL,
  `Email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `subitem`
--

CREATE TABLE `subitem` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `Sid` int(11) NOT NULL,
  `sTitle` varchar(50) NOT NULL,
  `percentage` float DEFAULT NULL,
  `CourseId` varchar(50) NOT NULL,
  `sectionNo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `teacher`
--

CREATE TABLE `teacher` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `staffid` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `teacher`
--

INSERT INTO `teacher` (`create_time`, `status`, `staffid`, `name`, `email`) VALUES
(NULL, NULL, '90641857', 'Kxcjkuzfv', 'Kxcjkuzfv@uic.edu.hk');

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `psw` varchar(50) NOT NULL,
  `usertype` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`create_time`, `status`, `username`, `psw`, `usertype`) VALUES
(NULL, NULL, 'Kxcjkuzfv@uic.edu.hk', '123456', 'teacher');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`CourseId`);

--
-- Indexes for table `courseteamstudent`
--
ALTER TABLE `courseteamstudent`
  ADD PRIMARY KEY (`rid`);

--
-- Indexes for table `course_student`
--
ALTER TABLE `course_student`
  ADD PRIMARY KEY (`rrrid`);

--
-- Indexes for table `course_teacher`
--
ALTER TABLE `course_teacher`
  ADD PRIMARY KEY (`rrid`);

--
-- Indexes for table `dividein`
--
ALTER TABLE `dividein`
  ADD PRIMARY KEY (`did`);

--
-- Indexes for table `invitation`
--
ALTER TABLE `invitation`
  ADD PRIMARY KEY (`iid`);

--
-- Indexes for table `leader`
--
ALTER TABLE `leader`
  ADD PRIMARY KEY (`lid`,`StudentID`);

--
-- Indexes for table `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`mid`);

--
-- Indexes for table `randnumber`
--
ALTER TABLE `randnumber`
  ADD PRIMARY KEY (`listid`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`StudentID`);

--
-- Indexes for table `subitem`
--
ALTER TABLE `subitem`
  ADD PRIMARY KEY (`Sid`);

--
-- Indexes for table `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`staffid`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `courseteamstudent`
--
ALTER TABLE `courseteamstudent`
  MODIFY `rid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- 使用表AUTO_INCREMENT `course_student`
--
ALTER TABLE `course_student`
  MODIFY `rrrid` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `course_teacher`
--
ALTER TABLE `course_teacher`
  MODIFY `rrid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用表AUTO_INCREMENT `dividein`
--
ALTER TABLE `dividein`
  MODIFY `did` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用表AUTO_INCREMENT `invitation`
--
ALTER TABLE `invitation`
  MODIFY `iid` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `leader`
--
ALTER TABLE `leader`
  MODIFY `lid` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `member`
--
ALTER TABLE `member`
  MODIFY `mid` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `randnumber`
--
ALTER TABLE `randnumber`
  MODIFY `listid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- 使用表AUTO_INCREMENT `subitem`
--
ALTER TABLE `subitem`
  MODIFY `Sid` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
