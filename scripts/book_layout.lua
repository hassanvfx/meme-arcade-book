local function page_break()
  return pandoc.RawBlock("openxml", [[<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:r><w:br w:type="page"/></w:r></w:p>]])
end

function Para(el)
  if pandoc.utils.stringify(el) == "\\newpage" then return page_break() end
end

function RawBlock(el)
  if el.text == "\\newpage" then return page_break() end
end

function Header(el)
  if el.level == 1 and not el.identifier:match("^about%-the%-author$") and not el.identifier:match("^acknowledgements$") then
    return {page_break(), el}
  end
end
