import { promises as fs } from "node:fs";
import path from "node:path";
import { serialize } from "next-mdx-remote/serialize";
import remarkGfm from "remark-gfm";
import rehypePrismPlus from "rehype-prism-plus";
import { docsManifest } from "@/lib/docs-manifest";

export async function getDocBySlug(slug: string) {
  const entry = docsManifest.find((doc) => doc.slug === slug);

  if (!entry) {
    return null;
  }

  // Updated to use .mdx extension
  const mdxFilename = entry.filename.replace(".md", ".mdx");
  const filePath = path.join(process.cwd(), "content", "docs", mdxFilename);

  try {
    const mdxContent = await fs.readFile(filePath, "utf8");

    // Serialize MDX content with plugins for syntax highlighting and GFM support
    const serialized = await serialize(mdxContent, {
      mdxOptions: {
        remarkPlugins: [remarkGfm],
        rehypePlugins: [
          [rehypePrismPlus, { defaultLanguage: "bash", showLineNumbers: false }],
        ],
      },
    });

    return {
      ...entry,
      serialized,
      filename: mdxFilename,
    };
  } catch (error) {
    console.error(`Error loading doc ${slug}:`, error);
    return null;
  }
}
