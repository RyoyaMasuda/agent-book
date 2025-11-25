import { WorkflowResult } from "../types/workflow";

// WorkflowResultsコンポーネントのProps（引数）の型定義
interface WorkflowResultsProps {
  result: WorkflowResult | null;
}

export const WorkflowResults = ({ result }: WorkflowResultsProps) => {
  if (!result) return null;

  // 実行中かどうかを判定
  const isRunning = result.message.includes("実行中");

  return (
    <div>
      <h2>
        📊 実行結果
      </h2>

      {/* 結果ステータス表示 */}
      <div>
        <div>
          {/* ステータスアイコン */}
          {isRunning ? (
            <div>
              <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"
                  fill="none" />
                <path fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </div>
          ) : result.success ? (
            <div>🎉</div>
          ) : (
            <div>🚨</div>
          )}
          <span>
            {result.message}
          </span>
        </div>

        {result.error && (
          <div>
            エラー詳細: {result.error}
          </div>
        )}
      </div>


      {/* Confluence検索結果 */}
      {result.confluencePages && result.confluencePages.length > 0 && (
        <div>
          <h3>
            <span>📚</span> Confluenceページ
          </h3>
          <div>
            {result.confluencePages.map((page, index) => (
              <div key={index}>
                <div>{page.title}</div>
                {page.message && (
                  <div>
                    {page.message}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
      {/* GitHub Issue結果 */}
      {result.githubIssues && result.githubIssues.length > 0 && (
        <div>
          <h3>
            <span>🐙</span> GitHub Issues
          </h3>
          <div>
            {result.githubIssues.map((issue, index) => (
              <div key={index}>
                <div>{issue.title}</div>
                <div>
                  <span>
                    #{issue.issueNumber}
                  </span>
                  {issue.issueUrl && (
                    <a
                      href={issue.issueUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Issueを開く
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                          d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
