// クライアントコンポーネントの宣言
"use client";

import { WorkflowFormData } from "../types/workflow";

// WorkflowFormコンポーネントのProps（引数）の型定義
interface WorkflowFormProps {
  formData: WorkflowFormData;
  isLoading: boolean;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
}

// WorkflowフォームのUIコンポーネント
export const WorkflowForm = ({
  formData,
  isLoading,
  onInputChange,
  onSubmit
}: WorkflowFormProps) => {
  // 入力項目に不足がないかチェック
  const isFormValid = formData.query && formData.owner && formData.repo;
  return (
    // フォームを定義
    <form onSubmit={onSubmit}>
      {/*Confluence検索クエリ欄*/}
      <div>
        <label htmlFor="query">
          🔍 検索クエリ
        </label>
        <input
          type="text"
          id="query"
          name="query"
          value={formData.query}
          onChange={onInputChange}
          placeholder="例: AIについての情報"
          required
        />
      </div>
      {/*GitHubアカウント名*/}
      <div>
        <div>
          <label htmlFor="owner">
            👤 GitHub Owner
          </label>
          <input
            type="text"
            id="owner"
            name="owner"
            value={formData.owner}
            onChange={onInputChange}
            placeholder="例: octocat"
            required
          />
        </div>
        {/*GitHubリポジトリ名*/}
        <div>
          <label htmlFor="repo">
            📁 Repository
          </label>
          <input
            type="text"
            id="repo"
            name="repo"
            value={formData.repo}
            onChange={onInputChange}
            placeholder="例: mastra_practice"
            required
          />
        </div>
      </div>
      {/* フォームの送信ボタン（ワークフローの実行ボタン） */}
      <div>
        <button
          type="submit"
          disabled={!isFormValid || isLoading}
          className={`
           px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-300 transform
           ${isFormValid && !isLoading
            ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 hover:scale-105 hover:shadow-lg focus:outline-none focus:ring-4 focus:ring-blue-300'
            : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }
         `}
        >
          {isLoading ? (
            <div className="flex items-center">
              <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"
                        fill="none"/>
                <path className="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              処理中...
            </div>
          ) : (
            <span className="flex items-center">
              ワークフロー実行 ✨
            </span>
          )}
        </button>
      </div>
    </form>
  );
}
