import jwt from "jsonwebtoken"
import { PrismaClient } from "@prisma/client"
import { Router } from "express"
import bcrypt from 'bcrypt'

const prisma = new PrismaClient()
const router = Router()


router.post("/", async (req, res) => {
  const { email, senha } = req.body

  // em termos de segurança, o recomendado é exibir uma mensagem padrão
  // a fim de evitar de dar "dicas" sobre o processo de login para hackers
  const mensaPadrao = "Login ou senha incorretos"

  if (!email || !senha) {
    // res.status(400).json({ erro: "Informe e-mail e senha do usuário" })
    res.status(400).json({ erro: mensaPadrao })
    return
  }

  try {
    const usuario = await prisma.usuario.findFirst({
      where: { email }
    })

    if (usuario == null) {
      // res.status(400).json({ erro: "E-mail inválido" })
      res.status(400).json({ erro: mensaPadrao })
      return
    }
  
    // se o e-mail existe, faz-se a comparação dos hashs
    if (bcrypt.compareSync(senha, usuario.senha)) {
      
      // se confere, gera e retorna o token
      const token = jwt.sign({
        userLogadoId: usuario.id,
        userLogadoNome: usuario.nome
      },
        process.env.JWT_KEY as string,
        { expiresIn: "1h" }
      )

      const ultimoAcesso = usuario.ultimoAcesso ? usuario.ultimoAcesso : "Este é seu primeiro login.";

      await prisma.usuario.update({
        where: { id: usuario.id },
        data: { ultimoAcesso: new Date() }
      });

      res.status(200).json({
        id: usuario.id,
        nome: usuario.nome,
        email: usuario.email,
        ultimoAcesso,
        token

      })  
    } else {
      // res.status(400).json({ erro: "Senha incorreta" })

      await prisma.log.create({
        data: { 
          descricao:"Tentativa de Acesso Inválida",
          complemento: `Funcionário: ${usuario.email}`,
          senhaAtual: senha,
          novaSenha: "",
          usuarioId: usuario.id
        }
      })

      router.post("/cadastrar", async (req, res) => {
        const { nome, email, senha } = req.body;
      
        if (!nome || !email || !senha) {
          res.status(400).json({ erro: "Informe o nome, e-mail e senha" });
          return;
        }
      
        try {
          const usuarioExistente = await prisma.usuario.findFirst({
            where: { email }
          });
      
          if (usuarioExistente) {
            res.status(400).json({ erro: "E-mail já cadastrado" });
            return;
          }
      
          const novoUsuario = await prisma.usuario.create({
            data: {
              nome,
              email,
              senha: bcrypt.hashSync(senha, 10)
            }
          });
      
          res.status(200).json({ mensagem: "Usuário cadastrado com sucesso" });
        } catch (error) {
          res.status(400).json({ erro: "Ocorreu um erro ao cadastrar o usuário" });
        }
      });

      res.status(400).json({ erro: mensaPadrao })
    }
  } catch (error) {
    res.status(400).json(error)
  }
})


function validaSenha(senha: string) {
  if (senha.length < 6) {
    return ["Erro... senha deve possuir, no mínimo, 6 caracteres"]
  }
}

router.put("/id", async (req, res) => {
  const { email, senhaAtual, novaSenha } = req.body;

  if (!email || !senhaAtual || !novaSenha) {
    res.status(400).json({ erro: "Informe o e-mail, senha atual e nova senha" });
    return;
  }

  try {
    const usuario = await prisma.usuario.findFirst({
      where: { email }
    });

    if (!usuario) {
      res.status(400).json({ erro: "Usuário não encontrado" });
      return;
    }

    if (!bcrypt.compareSync(senhaAtual, usuario.senha)) {
      res.status(400).json({ erro: "Senha atual incorreta" });
      return;
    }

    const novaSenhaCriptografada = bcrypt.hashSync(novaSenha, 10);

    await prisma.usuario.update({
      where: { id: usuario.id },
      data: { senha: novaSenhaCriptografada }
    });

    res.status(200).json({ mensagem: "Senha alterada com sucesso" });
  } catch (error) {
    res.status(400).json({ erro: "Ocorreu um erro ao alterar a senha" });
  }
});

export default router