-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 17, 2023 at 07:08 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ayura`
--

-- --------------------------------------------------------

--
-- Table structure for table `food_data`
--

CREATE TABLE `food_data` (
  `uid` int(11) NOT NULL,
  `food` text NOT NULL,
  `date_added` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `food_data`
--

INSERT INTO `food_data` (`uid`, `food`, `date_added`) VALUES
(1010, 'Gheela Pitha', '2023-03-07 08:54:32'),
(1010, 'Ghooghra', '2023-03-07 10:06:42'),
(1010, 'Kalakand', '2023-03-07 10:11:42'),
(1010, 'Jalebi', '2023-03-07 10:19:11'),
(1010, 'Jalebi', '2023-03-07 10:19:30'),
(1010, 'Bisi bele bath', '2023-03-07 13:11:11'),
(1010, 'Jalebi', '2023-03-09 05:59:40'),
(1010, 'Shrikhand', '2023-03-09 06:15:23'),
(1010, 'Koshambri', '2023-03-17 13:18:08'),
(1010, 'Jalebi', '2023-03-17 13:18:17'),
(1010, 'Kulfi falooda', '2023-03-17 15:33:20'),
(1010, 'Ghooghra', '2023-03-17 15:33:29');

-- --------------------------------------------------------

--
-- Table structure for table `test_result`
--

CREATE TABLE `test_result` (
  `uid` int(11) NOT NULL,
  `dosh_identified` varchar(5) NOT NULL,
  `vata` float NOT NULL,
  `pitta` float NOT NULL,
  `kapha` float NOT NULL,
  `test_date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `test_result`
--

INSERT INTO `test_result` (`uid`, `dosh_identified`, `vata`, `pitta`, `kapha`, `test_date`) VALUES
(1010, 'Vata', 45, 35, 20, '2023-03-02'),
(1010, 'Vata', 40, 35, 25, '2023-03-17'),
(1010, 'Kapha', 40, 40, 20, '2023-03-31');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `uid` int(10) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL,
  `age` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uid`, `username`, `password`, `email`, `age`) VALUES
(1010, 'bb', 'bbbb', 'bb@b.b', 21),
(1011, 'aa', 'aaaa', 'aa@a.a', 23),
(1013, 'cc', 'cccc', 'cc@c.c', 34);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `test_result`
--
ALTER TABLE `test_result`
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `uid` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1014;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
