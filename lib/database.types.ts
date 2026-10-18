// Tipos gerados a partir do banco do Supabase (projeto caderno-clinico).
// Para atualizar depois de mudar o banco: npx supabase gen types typescript --project-id xtlpmtylifbalzxnfkib

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  __InternalSupabase: {
    PostgrestVersion: '14.18'
  }
  public: {
    Tables: {
      aulas: {
        Row: {
          apostila_html: string | null
          criado_em: string
          id: string
          materia_id: string
          ordem: number
          pdf_caminho: string | null
          publicada: boolean
          resumo: string | null
          titulo: string
        }
        Insert: {
          apostila_html?: string | null
          criado_em?: string
          id: string
          materia_id: string
          ordem: number
          pdf_caminho?: string | null
          publicada?: boolean
          resumo?: string | null
          titulo: string
        }
        Update: {
          apostila_html?: string | null
          criado_em?: string
          id?: string
          materia_id?: string
          ordem?: number
          pdf_caminho?: string | null
          publicada?: boolean
          resumo?: string | null
          titulo?: string
        }
        Relationships: [
          {
            foreignKeyName: 'aulas_materia_id_fkey'
            columns: ['materia_id']
            isOneToOne: false
            referencedRelation: 'materias'
            referencedColumns: ['id']
          },
        ]
      }
      flashcards: {
        Row: { aula_id: string; frente: string; id: string; ordem: number; verso: string }
        Insert: { aula_id: string; frente: string; id: string; ordem?: number; verso: string }
        Update: { aula_id?: string; frente?: string; id?: string; ordem?: number; verso?: string }
        Relationships: [
          {
            foreignKeyName: 'flashcards_aula_id_fkey'
            columns: ['aula_id']
            isOneToOne: false
            referencedRelation: 'aulas'
            referencedColumns: ['id']
          },
        ]
      }
      historico_respostas: {
        Row: {
          correta: boolean
          escolhida: number
          id: number
          questao_id: string
          respondida_em: string
          user_id: string
        }
        Insert: {
          correta: boolean
          escolhida: number
          id?: number
          questao_id: string
          respondida_em?: string
          user_id?: string
        }
        Update: {
          correta?: boolean
          escolhida?: number
          id?: number
          questao_id?: string
          respondida_em?: string
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: 'historico_respostas_questao_id_fkey'
            columns: ['questao_id']
            isOneToOne: false
            referencedRelation: 'questoes'
            referencedColumns: ['id']
          },
        ]
      }
      materias: {
        Row: {
          cor_fim: string | null
          cor_inicio: string | null
          criado_em: string
          descricao: string | null
          id: string
          nome: string
          ordem: number
        }
        Insert: {
          cor_fim?: string | null
          cor_inicio?: string | null
          criado_em?: string
          descricao?: string | null
          id: string
          nome: string
          ordem?: number
        }
        Update: {
          cor_fim?: string | null
          cor_inicio?: string | null
          criado_em?: string
          descricao?: string | null
          id?: string
          nome?: string
          ordem?: number
        }
        Relationships: []
      }
      agenda_semanas: {
        Row: { semana: string; titulo: string | null; aviso: string | null; texto: string | null; atualizado_em: string }
        Insert: { semana: string; titulo?: string | null; aviso?: string | null; texto?: string | null; atualizado_em?: string }
        Update: { semana?: string; titulo?: string | null; aviso?: string | null; texto?: string | null; atualizado_em?: string }
        Relationships: []
      }
      agenda_eventos: {
        Row: {
          id: number; semana: string; data: string; inicio: string | null; fim: string | null; materia: string | null
          tipo: string; titulo: string; professor: string | null; local: string | null; grupos: number[] | null
          cancelado: boolean; notas: string[] | null; ordem: number
        }
        Insert: {
          id?: never; semana: string; data: string; inicio?: string | null; fim?: string | null; materia?: string | null
          tipo?: string; titulo: string; professor?: string | null; local?: string | null; grupos?: number[] | null
          cancelado?: boolean; notas?: string[] | null; ordem?: number
        }
        Update: {
          id?: never; semana?: string; data?: string; inicio?: string | null; fim?: string | null; materia?: string | null
          tipo?: string; titulo?: string; professor?: string | null; local?: string | null; grupos?: number[] | null
          cancelado?: boolean; notas?: string[] | null; ordem?: number
        }
        Relationships: []
      }
      perfis: {
        Row: { admin: boolean; criado_em: string; id: string; nome: string | null; grupo: number | null }
        Insert: { admin?: boolean; criado_em?: string; id: string; nome?: string | null; grupo?: number | null }
        Update: { admin?: boolean; criado_em?: string; id?: string; nome?: string | null; grupo?: number | null }
        Relationships: []
      }
      recados: {
        Row: { id: string; questao_id: string; user_id: string; autor: string; tipo: string; texto: string; status: string; criado_em: string }
        Insert: { id?: string; questao_id: string; user_id?: string; autor?: string; tipo: string; texto: string; status?: string; criado_em?: string }
        Update: { id?: string; questao_id?: string; user_id?: string; autor?: string; tipo?: string; texto?: string; status?: string; criado_em?: string }
        Relationships: []
      }
      recados_uteis: {
        Row: { recado_id: string; user_id: string }
        Insert: { recado_id: string; user_id?: string }
        Update: { recado_id?: string; user_id?: string }
        Relationships: []
      }
      questoes: {
        Row: {
          alternativas: Json
          aula_id: string | null
          comentario: string | null
          correta: number
          enunciado: string
          fonte: string | null
          id: string
          materia_id: string
          ordem: number
          origem: string | null
          por_que_erradas: string | null
          prova: string | null
          tema: string | null
        }
        Insert: {
          alternativas: Json
          aula_id?: string | null
          comentario?: string | null
          correta: number
          enunciado: string
          fonte?: string | null
          id: string
          materia_id: string
          ordem?: number
          origem?: string | null
          por_que_erradas?: string | null
          prova?: string | null
          tema?: string | null
        }
        Update: {
          alternativas?: Json
          aula_id?: string | null
          comentario?: string | null
          correta?: number
          enunciado?: string
          fonte?: string | null
          id?: string
          materia_id?: string
          ordem?: number
          origem?: string | null
          por_que_erradas?: string | null
          prova?: string | null
          tema?: string | null
        }
        Relationships: [
          {
            foreignKeyName: 'questoes_aula_id_fkey'
            columns: ['aula_id']
            isOneToOne: false
            referencedRelation: 'aulas'
            referencedColumns: ['id']
          },
          {
            foreignKeyName: 'questoes_materia_id_fkey'
            columns: ['materia_id']
            isOneToOne: false
            referencedRelation: 'materias'
            referencedColumns: ['id']
          },
        ]
      }
      respostas: {
        Row: {
          correta: boolean
          escolhida: number
          questao_id: string
          respondida_em: string
          tentativas: number
          user_id: string
        }
        Insert: {
          correta: boolean
          escolhida: number
          questao_id: string
          respondida_em?: string
          tentativas?: number
          user_id?: string
        }
        Update: {
          correta?: boolean
          escolhida?: number
          questao_id?: string
          respondida_em?: string
          tentativas?: number
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: 'respostas_questao_id_fkey'
            columns: ['questao_id']
            isOneToOne: false
            referencedRelation: 'questoes'
            referencedColumns: ['id']
          },
        ]
      }
      revisoes: {
        Row: {
          facilidade: number
          flashcard_id: string
          intervalo_dias: number
          lapsos: number
          proxima_revisao: string
          repeticoes: number
          ultima_revisao: string
          user_id: string
        }
        Insert: {
          facilidade?: number
          flashcard_id: string
          intervalo_dias?: number
          lapsos?: number
          proxima_revisao: string
          repeticoes?: number
          ultima_revisao?: string
          user_id?: string
        }
        Update: {
          facilidade?: number
          flashcard_id?: string
          intervalo_dias?: number
          lapsos?: number
          proxima_revisao?: string
          repeticoes?: number
          ultima_revisao?: string
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: 'revisoes_flashcard_id_fkey'
            columns: ['flashcard_id']
            isOneToOne: false
            referencedRelation: 'flashcards'
            referencedColumns: ['id']
          },
        ]
      }
    }
    Views: {
      flashcards_do_aluno: {
        Row: {
          aula_id: string | null
          aula_ordem: number | null
          aula_titulo: string | null
          facilidade: number | null
          frente: string | null
          id: string | null
          intervalo_dias: number | null
          lapsos: number | null
          materia_id: string | null
          materia_nome: string | null
          materia_ordem: number | null
          ordem: number | null
          proxima_revisao: string | null
          repeticoes: number | null
          ultima_revisao: string | null
          verso: string | null
        }
        Relationships: []
      }
      progresso_aulas: {
        Row: {
          acertos: number | null
          aula_id: string | null
          cards_estudados: number | null
          cards_vencidos: number | null
          materia_id: string | null
          ordem: number | null
          respondidas: number | null
          titulo: string | null
          total_cards: number | null
          total_questoes: number | null
          ultima_atividade: string | null
        }
        Relationships: []
      }
      questoes_do_aluno: {
        Row: {
          acertou: boolean | null
          alternativas: Json | null
          aula_id: string | null
          comentario: string | null
          correta: number | null
          enunciado: string | null
          escolhida: number | null
          fonte: string | null
          id: string | null
          materia_id: string | null
          ordem: number | null
          origem: string | null
          por_que_erradas: string | null
          prova: string | null
          respondida_em: string | null
          tema: string | null
          tentativas: number | null
        }
        Relationships: []
      }
      progresso_materias: {
        Row: {
          acertos: number | null
          materia_id: string | null
          respondidas: number | null
          total_questoes: number | null
        }
        Relationships: []
      }
      progresso_temas: {
        Row: {
          acertos: number | null
          materia_id: string | null
          respondidas: number | null
          tema: string | null
          total_questoes: number | null
        }
        Relationships: []
      }
      progresso_tentativas: {
        Row: {
          acertos_primeira: number | null
          materia_id: string | null
          primeiras: number | null
          tentativas: number | null
        }
        Relationships: []
      }
    }
    Functions: { [_ in never]: never }
    Enums: { [_ in never]: never }
    CompositeTypes: { [_ in never]: never }
  }
}
