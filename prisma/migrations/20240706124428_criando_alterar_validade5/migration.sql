/*
  Warnings:

  - You are about to alter the column `validade` on the `produtos` table. The data in that column could be lost. The data in that column will be cast from `VarChar(10)` to `Decimal(9,2)`.

*/
-- AlterTable
ALTER TABLE `produtos` MODIFY `validade` DECIMAL(9, 2) NOT NULL;
