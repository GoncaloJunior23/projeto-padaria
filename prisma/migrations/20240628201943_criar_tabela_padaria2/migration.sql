/*
  Warnings:

  - You are about to alter the column `validade` on the `produtos` table. The data in that column could be lost. The data in that column will be cast from `SmallInt` to `VarChar(10)`.

*/
-- AlterTable
ALTER TABLE `produtos` MODIFY `validade` VARCHAR(10) NOT NULL;
