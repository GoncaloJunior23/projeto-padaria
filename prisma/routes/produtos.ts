import { PrismaClient } from "@prisma/client"
import { Router } from "express"

import { verificaToken } from "../middewares/verificaToken"

const prisma = new PrismaClient()

async function main() {
  /***********************************/
  /* SOFT DELETE MIDDLEWARE */
  /***********************************/
  prisma.$use(async(params, next) => {
    // Check incoming query type
    if (params.model == 'Produto') {
      if (params.action == 'delete') {
        // Delete queries
        // Change action to an update
        params.action = 'update'
        params.args['data'] = { deleted: true }
      }
    }
    return next(params)
  })
}
main()

const router = Router()

router.get("/", async (req, res) => {
  try {
    const produtos = await prisma.produto.findMany({
      where: { deleted: false }
    })
    res.status(200).json(produtos)
  } catch (error) {
    res.status(400).json(error)
  }
})

router.post("/", verificaToken, async (req: any, res) => {
  const { nome, tipo, validade, preco } = req.body

  const { userLogadoId } = req

  console.log("=================================")
  console.log(userLogadoId)
  console.log("=================================")

  if (!nome || !tipo || !validade || !preco) {
    res.status(400).json({ erro: "Informe nome, tipo, validade e preco" })
    return
  }

  try {
    const produtos = await prisma.produto.create({
      data: { nome, tipo, validade, preco, usuarioId: userLogadoId }
    })
    res.status(201).json(produtos)
  } catch (error) {
    res.status(400).json(error)
  }
})

router.delete("/:id", async (req, res) => {
  const { id } = req.params;

  try {
    const produtos = await prisma.produto.delete({
      where: { id: Number(id) },
    });
    res.status(200).json(produtos);
  } catch (error) {
    res.status(400).json(error);
  }
});

router.put("/:id", async (req, res) => {
  const { id } = req.params;
  const { preco } = req.body; // Apenas o preço será atualizado

  if (!preco) {
    res.status(400).json({ erro: "Informe o novo preço" });
    return;
  }

  try {
    const produto = await prisma.produto.update({
      where: { id: Number(id) },
      data: { preco: preco }
    });
    res.status(200).json(produto);
  } catch (error) {
    res.status(400).json(error);
  }
});

export default router