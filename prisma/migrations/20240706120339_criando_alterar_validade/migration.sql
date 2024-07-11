/*
  Warnings:

  - You are about to alter the column `validade` on the `produtos` table. The data in that column could be lost. The data in that column will be cast from `VarChar(10)` to `Int`.

*/
-- AlterTable
ALTER TABLE `produtos` MODIFY `validade` INTEGER NOT NULL;
