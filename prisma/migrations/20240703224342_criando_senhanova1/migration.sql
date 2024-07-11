/*
  Warnings:

  - You are about to drop the column `acesso` on the `logs` table. All the data in the column will be lost.
  - Added the required column `novaSenha` to the `logs` table without a default value. This is not possible if the table is not empty.
  - Added the required column `senhaAtual` to the `logs` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE `logs` DROP COLUMN `acesso`,
    ADD COLUMN `novaSenha` VARCHAR(60) NOT NULL,
    ADD COLUMN `senhaAtual` VARCHAR(60) NOT NULL;
